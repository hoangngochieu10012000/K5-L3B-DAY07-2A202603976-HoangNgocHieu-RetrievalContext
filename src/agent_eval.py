"""Evaluate Agent on Dev and Test benchmarks with real LLM and retrieval."""
import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

from .agent import NvidiaGemmaController, load_env_file
from .embeddings import Day6Embedder
from .retrievers import DenseRetriever, BM25Retriever, HybridRetriever

# Add starter to path
sys.path.append(str(Path(__file__).parent.parent / "starter"))
from agentic import run_agent
from agent_metrics import aggregate

logger = logging.getLogger(__name__)


class AgentRetrieverAdapter:
    """Adapter wrapping our retriever to match starter agentic Retriever protocol."""

    def __init__(self, retriever):
        self.retriever = retriever

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        results = self.retriever.search(query, top_k=top_k, filters=filters)
        return results


def grade_answer(
    case: dict[str, Any],
    trace: dict[str, Any],
    gold_question: dict[str, Any] | None
) -> tuple[int | None, list[bool], bool | None]:
    """Grade agent response against gold standard according to Day 7 Rubric.

    Returns:
        (answer_grade: 0|1|2, citation_support: list[bool], abstention_correct: bool|None)
    """
    answerable = case.get("answerable", True)
    status = trace.get("status")
    answer = trace.get("answer", "")
    citations = trace.get("citations", [])
    events = trace.get("events", [])

    # Get cumulative context
    context = ""
    for e in reversed(events):
        if e.get("event") == "search" and e.get("context"):
            context = e.get("context")
            break

    # 1. Audit citations: does each citation exist in context and support the statement?
    citation_support = []
    for c_id in citations:
        in_ctx = c_id in context
        citation_support.append(in_ctx)

    if not answerable:
        # For unanswerable questions: abstention is correct if status is 'abstain' or explicitly states absence
        is_abstain = (status == "abstain") or ("không đủ bằng chứng" in answer.lower())
        return None, citation_support, is_abstain
    else:
        # Answerable questions
        if status == "abstain":
            # Abstaining on an answerable question is graded 0 per rubric
            return 0, citation_support, None

        if not gold_question:
            return 1, citation_support, None

        expected = gold_question.get("expected_answer", "").lower()
        gold_evidences = [g.get("evidence", "").lower() for g in gold_question.get("gold", [])]
        ans_lower = answer.lower()

        # Grade criteria:
        # 2: Correct, grounded, cites valid evidence
        # 1: Partially correct or missing details
        # 0: Incorrect or hallucinated
        all_cites_valid = all(citation_support) if citation_support else False
        has_key_evidence = any(e in ans_lower or any(word in ans_lower for word in e.split()[:4]) for e in gold_evidences)
        matches_expected = any(word in ans_lower for word in expected.split() if len(word) > 3)

        if all_cites_valid and (has_key_evidence or matches_expected):
            grade = 2
        elif has_key_evidence or matches_expected:
            grade = 1
        else:
            grade = 0

        return grade, citation_support, None


def run_benchmark(
    controller: NvidiaGemmaController,
    retriever,
    cases: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    split: str,
    output_dir: Path,
    max_searches: int = 2,
    top_k: int = 3,
    budget: int = 1200
):
    split_cases = [c for c in cases if c.get("split") == split]
    questions_map = {q["id"]: q for q in questions}

    traces = []
    reviews = []
    adapter = AgentRetrieverAdapter(retriever)

    print(f"\nRunning Agent benchmark on split: {split.upper()} ({len(split_cases)} cases)...")

    for i, case in enumerate(split_cases, start=1):
        cid = case["id"]
        q_text = case["question"]
        print(f"[{i}/{len(split_cases)}] Query {cid}: '{q_text}'...")

        gold_q = questions_map.get(cid)
        filters = gold_q.get("filter") if gold_q else None

        start_t = time.perf_counter()
        try:
            result = run_agent(
                question=q_text,
                controller=controller,
                retriever=adapter,
                filters=filters,
                max_searches=max_searches,
                top_k=top_k,
                budget=budget
            )
            elapsed_s = time.perf_counter() - start_t
            result["query_id"] = cid
            result["elapsed_s"] = elapsed_s

        except Exception as e:
            logger.error(f"Error on {cid}: {e}")
            result = {
                "query_id": cid,
                "status": "error",
                "answer": f"Error: {str(e)}",
                "citations": [],
                "events": [],
                "elapsed_s": time.perf_counter() - start_t
            }

        traces.append(result)

        if result.get("status") != "error":
            grade, cite_sup, abs_correct = grade_answer(case, result, gold_q)
            review = {
                "query_id": cid,
                "citation_support": cite_sup
            }
            if grade is not None:
                review["answer_grade"] = grade
            if abs_correct is not None:
                review["abstention_correct"] = abs_correct

            reviews.append(review)

            print(f"   -> Status: {result['status']}, Citations: {result['citations']}, Grade: {grade}, AbstainCorrect: {abs_correct}")

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "traces.json", "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    with open(output_dir / "reviews.json", "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    # Compute aggregate metrics
    report = aggregate(split_cases, traces, reviews)
    report["split"] = split

    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n---------------- AGGREGATE SUMMARY ----------------")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description="Evaluate Agent on Day 7 benchmark")
    parser.add_argument("--split", choices=("dev", "test", "both"), default="both")
    parser.add_argument("--retriever", choices=("dense", "hybrid"), default="hybrid")
    parser.add_argument("--budget", type=int, default=1200)
    parser.add_argument("--top_k", type=int, default=3)
    args = parser.parse_args()

    # Load data
    cases = json.loads(Path("data/agent_cases.json").read_text(encoding="utf-8"))
    questions = json.loads(Path("data/questions.json").read_text(encoding="utf-8"))
    chunks = json.loads(Path("data/chunks.json").read_text(encoding="utf-8"))

    print("Initializing Controller and Retriever...")
    controller = NvidiaGemmaController()
    embedder = Day6Embedder()
    dense = DenseRetriever(qdrant_path="data/qdrant_db", embedder=embedder)

    if args.retriever == "hybrid":
        bm25 = BM25Retriever(chunks=chunks)
        retriever = HybridRetriever(dense_retriever=dense, bm25_retriever=bm25, rrf_k=60)
        retriever_name = "hybrid_rrf"
    else:
        retriever = dense
        retriever_name = "dense"

    results_dir = Path("results") / f"agent_{retriever_name}"

    if args.split in ("dev", "both"):
        run_benchmark(
            controller=controller,
            retriever=retriever,
            cases=cases,
            questions=questions,
            split="dev",
            output_dir=results_dir / "dev",
            budget=args.budget,
            top_k=args.top_k
        )

    if args.split in ("test", "both"):
        run_benchmark(
            controller=controller,
            retriever=retriever,
            cases=cases,
            questions=questions,
            split="test",
            output_dir=results_dir / "test",
            budget=args.budget,
            top_k=args.top_k
        )

    dense.close()


if __name__ == "__main__":
    main()
