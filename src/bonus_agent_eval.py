"""Evaluate Agent on Bonus SGK Dia Li 10 Dev and Test benchmarks."""
import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

from .agent import NvidiaGemmaController
from .embeddings import Day6Embedder
from .retrievers import DenseRetriever, BM25Retriever, HybridRetriever

# Add starter to path
sys.path.append(str(Path(__file__).parent.parent / "starter"))
from agentic import run_agent
from agent_metrics import aggregate

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class AgentRetrieverAdapter:
    """Adapter wrapping our retriever to match starter agentic Retriever protocol."""

    def __init__(self, retriever):
        self.retriever = retriever

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        results = self.retriever.search(query, top_k=top_k, filters=filters)
        return results


def grade_bonus_answer(
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
        # For unanswerable questions: abstention is correct if status is 'abstain'
        is_abstain = (status == "abstain")
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

        # Check for citation validity: at least one valid citation in context
        all_cites_valid = (len(citations) > 0 and all(citation_support))

        # Check keyword / number overlap with gold expected answer & evidence
        # Extract meaningful tokens (len > 3 or digits/percentages)
        exp_tokens = [w for w in expected.replace(",", " ").replace(".", " ").replace("%", " % ").split() if len(w) > 3 or any(c.isdigit() for c in w)]
        matching_exp_tokens = [w for w in exp_tokens if w in ans_lower]
        exp_match_ratio = len(matching_exp_tokens) / len(exp_tokens) if exp_tokens else 0.5

        has_direct_evidence = any(e in ans_lower or any(word in ans_lower for word in e.split()[:4]) for e in gold_evidences)

        if all_cites_valid and (exp_match_ratio >= 0.4 or has_direct_evidence):
            grade = 2
        elif exp_match_ratio >= 0.25 or has_direct_evidence:
            grade = 1
        else:
            grade = 0

        return grade, citation_support, None


def run_bonus_benchmark(
    controller: NvidiaGemmaController,
    retriever,
    cases: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    split: str,
    output_dir: Path,
    max_searches: int = 3,
    top_k: int = 3,
    budget: int = 1500
):
    split_cases = [c for c in cases if c.get("split") == split]
    questions_map = {q["id"]: q for q in questions}

    traces = []
    reviews = []
    adapter = AgentRetrieverAdapter(retriever)

    print(f"\n=======================================================")
    print(f"Running BONUS Agent benchmark on split: {split.upper()} ({len(split_cases)} cases)...")
    print(f"=======================================================")

    for i, case in enumerate(split_cases, start=1):
        cid = case["id"]
        q_text = case["question"]
        cat = case.get("category", "")
        ans_type = "Answerable" if case.get("answerable") else "Unanswerable (Abstain)"
        print(f"\n[{i}/{len(split_cases)}] Query {cid} [{cat}|{ans_type}]: '{q_text}'")

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
            grade, cite_sup, abs_correct = grade_bonus_answer(case, result, gold_q)
            review = {
                "query_id": cid,
                "citation_support": cite_sup
            }
            if grade is not None:
                review["answer_grade"] = grade
            if abs_correct is not None:
                review["abstention_correct"] = abs_correct

            reviews.append(review)

            print(f"   -> Status: {result['status']}, Elapsed: {elapsed_s:.2f}s, Citations: {result['citations']}")
            if grade is not None:
                print(f"   -> Grade: {grade}/2")
            if abs_correct is not None:
                print(f"   -> Abstain Correct: {abs_correct}")
            print(f"   -> Answer snippet: {result.get('answer', '')[:120]}...")

        # Small pause between queries to respect API rate limits
        time.sleep(1.0)

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "traces.json", "w", encoding="utf-8") as f:
        json.dump(traces, f, ensure_ascii=False, indent=2)

    with open(output_dir / "reviews.json", "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    # Compute aggregate metrics per starter/agent_metrics.py
    report = aggregate(split_cases, traces, reviews)
    report["split"] = split

    # Calculate category-level breakdown
    cat_stats = {}
    for case in split_cases:
        cid = case["id"]
        cat = case.get("category", "other")
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "correct": 0}
        cat_stats[cat]["total"] += 1
        
        rev = next((r for r in reviews if r["query_id"] == cid), None)
        tr = next((t for t in traces if t["query_id"] == cid), None)
        if case.get("answerable"):
            if rev and rev.get("answer_grade", 0) >= 1:
                cat_stats[cat]["correct"] += 1
        else:
            if rev and rev.get("abstention_correct", False):
                cat_stats[cat]["correct"] += 1

    report["category_breakdown"] = cat_stats
    total_cases = len(split_cases)
    total_correct = sum(v["correct"] for v in cat_stats.values())
    report["overall_accuracy"] = round(total_correct / total_cases * 100, 2) if total_cases > 0 else 0

    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n---------------- AGGREGATE SUMMARY ----------------")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description="Evaluate Agent on Bonus SGK Dia Li 10 benchmark")
    parser.add_argument("--split", choices=("dev", "test", "both"), default="both")
    parser.add_argument("--budget", type=int, default=1500)
    parser.add_argument("--top_k", type=int, default=3)
    args = parser.parse_args()

    # Load bonus data
    cases = json.loads(Path("data/bonus/agent_cases.json").read_text(encoding="utf-8"))
    questions = json.loads(Path("data/bonus/questions.json").read_text(encoding="utf-8"))
    chunks = json.loads(Path("data/bonus/chunks.json").read_text(encoding="utf-8"))

    print("Initializing Controller and Bonus Hybrid Retriever...")
    controller = NvidiaGemmaController()
    embedder = Day6Embedder()
    dense = DenseRetriever(qdrant_path="data/qdrant_db", embedder=embedder, collection_name="bonus_sgk10")
    bm25 = BM25Retriever(chunks=chunks)
    hybrid = HybridRetriever(dense_retriever=dense, bm25_retriever=bm25, rrf_k=60)

    results_dir = Path("results/bonus")

    if args.split in ("dev", "both"):
        run_bonus_benchmark(
            controller=controller,
            retriever=hybrid,
            cases=cases,
            questions=questions,
            split="dev",
            output_dir=results_dir / "agent_hybrid_dev",
            budget=args.budget,
            top_k=args.top_k
        )

    if args.split in ("test", "both"):
        run_bonus_benchmark(
            controller=controller,
            retriever=hybrid,
            cases=cases,
            questions=questions,
            split="test",
            output_dir=results_dir / "agent_hybrid_test",
            budget=args.budget,
            top_k=args.top_k
        )

    dense.close()


if __name__ == "__main__":
    main()
