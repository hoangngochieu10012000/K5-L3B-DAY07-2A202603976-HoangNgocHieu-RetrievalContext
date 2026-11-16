"""Test google/gemma-4-31b-it on Day 7 Agent flow."""
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import NvidiaGemmaController

ctl = NvidiaGemmaController()

q = "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo nào và bởi ai?"
print(f"Testing Question: {q}")

# Step 1: Decision on empty context
t0 = time.time()
action1 = ctl.decide(q, history=[])
print(f"Step 1 time: {time.time()-t0:.2f}s")
print(f"Step 1 Action: {action1}")

# Step 2: Decision with retrieved context
dummy_context = (
    "[aio2025-tutorial-rag_p4_b00 | data/AIO2025_Tutorial_RAG.pdf | page 4]\n"
    "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo khoa học “Retrieval-\n"
    "Augmented Generation for Knowledge-Intensive NLP Tasks” bởi Patrick Lewis và các cộng\n"
    "sự tại Facebook AI Research (FAIR) vào năm 2020."
)
history = [{
    "tool": "search",
    "queries": [action1.get("query", q)],
    "context": dummy_context,
    "context_ids": ["aio2025-tutorial-rag_p4_b00"]
}]

t1 = time.time()
action2 = ctl.decide(q, history=history)
print(f"Step 2 time: {time.time()-t1:.2f}s")
print(f"Step 2 Action: {action2}")
