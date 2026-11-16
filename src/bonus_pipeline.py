"""Retrieval evaluation on Bonus SGK Dia li 10 dataset."""
import json
import logging
import os
import sys
import time
from pathlib import Path

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "starter"))

from baseline import hit, pack_context
from src.embeddings import Day6Embedder
from src.retrievers import DenseRetriever, BM25Retriever, HybridRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BONUS_DIR = ROOT_DIR / "data" / "bonus"
RESULTS_DIR = ROOT_DIR / "results" / "bonus"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

with open(BONUS_DIR / "chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

with open(BONUS_DIR / "questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

embedder = Day6Embedder()
dense = DenseRetriever(qdrant_path="data/qdrant_db", collection_name="bonus_sgk10", embedder=embedder)
bm25 = BM25Retriever(chunks)
hybrid = HybridRetriever(dense, bm25, rrf_k=60)

for split in ("dev", "test"):
    split_questions = [q for q in questions if q.get("split") == split]
    logger.info(f"Evaluating {len(split_questions)} questions on split: {split}")

    for retriever_name, retriever in [
        ("dense", dense),
        ("bm25", bm25),
        ("hybrid_rrf", hybrid)
    ]:
        traces = []
        for q in split_questions:
            t0 = time.perf_counter()
            results = retriever.search(q["question"], top_k=3)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            context, context_ids = pack_context(results, budget=1200)
            marked = [{**c, "hit": hit(c, q["gold"])} for c in results]
            traces.append({
                "query_id": q["id"],
                "category": q.get("category"),
                "question": q["question"],
                "results": marked,
                "hit1": bool(marked and marked[0]["hit"]),
                "hit3": any(c["hit"] for c in marked),
                "context_hit": any(c["hit"] and c["id"] in context_ids for c in marked),
                "elapsed_ms": elapsed_ms
            })

        hit1_count = sum(t["hit1"] for t in traces)
        hit3_count = sum(t["hit3"] for t in traces)
        ctx_count = sum(t["context_hit"] for t in traces)
        n = len(traces)
        logger.info(
            f"[{split.upper()}] {retriever_name.upper()}: "
            f"Hit@1={hit1_count}/{n} ({hit1_count/n:.1%}) | "
            f"Hit@3={hit3_count}/{n} ({hit3_count/n:.1%}) | "
            f"Context Evidence={ctx_count}/{n} ({ctx_count/n:.1%})"
        )

        out_dir = RESULTS_DIR / f"{retriever_name}_{split}"
        out_dir.mkdir(parents=True, exist_ok=True)
        summary = {
            "retriever": retriever_name,
            "split": split,
            "n": n,
            "hit1": hit1_count,
            "hit1_rate": hit1_count / n,
            "hit3": hit3_count,
            "hit3_rate": hit3_count / n,
            "context_hit": ctx_count,
            "context_evidence_rate": ctx_count / n
        }
        with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        with open(out_dir / "traces.json", "w", encoding="utf-8") as f:
            json.dump(traces, f, ensure_ascii=False, indent=2)

logger.info("Bonus Retrieval pipeline evaluation complete!")
