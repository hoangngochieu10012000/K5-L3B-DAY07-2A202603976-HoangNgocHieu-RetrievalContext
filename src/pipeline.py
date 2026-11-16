"""Experiment pipeline for comparing retrieval methods on Day 7 benchmark."""
import argparse
import json
import statistics
import time
from pathlib import Path
from typing import Any

from .embeddings import Day6Embedder
from .retrievers import DenseRetriever, BM25Retriever, HybridRetriever, QueryTransformHybridRetriever

# Add starter for pack_context and hit
import sys
sys.path.append(str(Path(__file__).parent.parent / "starter"))
from baseline import pack_context, hit, validate


def run_experiment(
    retriever_name: str,
    retriever_fn,
    questions: list[dict[str, Any]],
    split: str,
    output_dir: Path,
    budget: int = 800,
    top_k: int = 3,
    use_filter: bool = False
) -> dict[str, Any]:
    """Run a retrieval configuration on a split, compute metrics, and save traces."""
    selected_questions = [q for q in questions if q.get("split") == split]
    if not selected_questions:
        raise ValueError(f"No questions found for split '{split}'")

    traces = []
    latencies = []

    for q in selected_questions:
        filters = q.get("filter") if use_filter else None
        start = time.perf_counter()
        results = retriever_fn(q["question"], top_k=top_k, filters=filters)
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)

        context, context_ids = pack_context(results, budget=budget)

        marked_results = []
        for c in results:
            is_hit = hit(c, q["gold"])
            marked_results.append({
                **c,
                "hit": is_hit
            })

        hit1 = bool(marked_results and marked_results[0]["hit"])
        hit3 = any(c["hit"] for c in marked_results[:3])
        context_hit = any(c["hit"] and c["id"] in context_ids for c in marked_results)

        traces.append({
            "query_id": q["id"],
            "split": split,
            "question": q["question"],
            "strategy": retriever_name,
            "top_k": top_k,
            "budget_chars": budget,
            "filter_applied": filters,
            "gold": q["gold"],
            "results": marked_results,
            "context": context,
            "context_ids": context_ids,
            "context_chars": len(context),
            "elapsed_ms": elapsed_ms,
            "hit1": hit1,
            "hit3": hit3,
            "context_hit": context_hit
        })

    n = len(traces)
    hit1_count = sum(t["hit1"] for t in traces)
    hit3_count = sum(t["hit3"] for t in traces)
    context_hit_count = sum(t["context_hit"] for t in traces)

    summary = {
        "strategy": retriever_name,
        "split": split,
        "n": n,
        "hit1": hit1_count,
        "hit1_rate": hit1_count / n if n > 0 else 0.0,
        "hit3": hit3_count,
        "hit3_rate": hit3_count / n if n > 0 else 0.0,
        "context_hit": context_hit_count,
        "context_evidence_rate": context_hit_count / n if n > 0 else 0.0,
        "avg_context_chars": statistics.mean(t["context_chars"] for t in traces),
        "median_ms": statistics.median(latencies),
        "cost_usd": 0.0
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "traces.json", "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return summary


def main():
    chunks_path = Path("data/chunks.json")
    questions_path = Path("data/questions.json")

    chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    questions = json.loads(questions_path.read_text(encoding="utf-8"))

    print("Initializing embedder and retrievers...")
    embedder = Day6Embedder()
    dense = DenseRetriever(qdrant_path="data/qdrant_db", embedder=embedder)
    bm25 = BM25Retriever(chunks=chunks)
    hybrid = HybridRetriever(dense_retriever=dense, bm25_retriever=bm25, rrf_k=60)
    query_transform = QueryTransformHybridRetriever(hybrid_retriever=hybrid)

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    configs_dev = [
        ("method_dense", lambda q, top_k, filters: dense.search(q, top_k=top_k, filters=None), False),
        ("method_bm25", lambda q, top_k, filters: bm25.search(q, top_k=top_k, filters=None), False),
        ("method_hybrid_rrf", lambda q, top_k, filters: hybrid.search(q, top_k=top_k, filters=None), False),
        ("improve_dense_filter", lambda q, top_k, filters: dense.search(q, top_k=top_k, filters=filters), True),
        ("improve_query_transform_hybrid", lambda q, top_k, filters: query_transform.search(q, top_k=top_k, filters=None), False),
    ]

    summaries = []
    print("\n=================== DEV BENCHMARKS ===================")
    for name, fn, use_filt in configs_dev:
        out_path = results_dir / f"{name}_dev"
        s = run_experiment(name, fn, questions, split="dev", output_dir=out_path, use_filter=use_filt)
        summaries.append(s)
        print(f"[{s['strategy']}] Hit@1: {s['hit1']}/{s['n']} ({s['hit1_rate']*100:.1f}%) | "
              f"Hit@3: {s['hit3']}/{s['n']} ({s['hit3_rate']*100:.1f}%) | "
              f"ContextRate: {s['context_hit']}/{s['n']} ({s['context_evidence_rate']*100:.1f}%) | "
              f"Latency: {s['median_ms']:.2f}ms")

    # Pick the best configuration from Dev to evaluate on Test
    # Ranking by Hit@3 then Context Evidence Rate
    best_config_name = max(summaries, key=lambda s: (s["hit3_rate"], s["context_evidence_rate"], s["hit1_rate"]))["strategy"]
    print(f"\n--> Best Configuration selected on Dev: {best_config_name}")

    print("\n=================== TEST BENCHMARKS ===================")
    # Test evaluation for Baseline (dense without filter) and Chosen Config
    test_configs = [
        ("baseline_dense_test", lambda q, top_k, filters: dense.search(q, top_k=top_k, filters=None), False),
        ("chosen_hybrid_rrf_test", lambda q, top_k, filters: hybrid.search(q, top_k=top_k, filters=None), False),
        ("chosen_query_transform_test", lambda q, top_k, filters: query_transform.search(q, top_k=top_k, filters=None), False),
    ]

    for name, fn, use_filt in test_configs:
        out_path = results_dir / name
        s = run_experiment(name, fn, questions, split="test", output_dir=out_path, use_filter=use_filt)
        print(f"[{s['strategy']}] Hit@1: {s['hit1']}/{s['n']} ({s['hit1_rate']*100:.1f}%) | "
              f"Hit@3: {s['hit3']}/{s['n']} ({s['hit3_rate']*100:.1f}%) | "
              f"ContextRate: {s['context_hit']}/{s['n']} ({s['context_evidence_rate']*100:.1f}%) | "
              f"Latency: {s['median_ms']:.2f}ms")

    dense.close()
    print("\nRetrieval experiments complete! All traces saved in results/")


if __name__ == "__main__":
    main()
