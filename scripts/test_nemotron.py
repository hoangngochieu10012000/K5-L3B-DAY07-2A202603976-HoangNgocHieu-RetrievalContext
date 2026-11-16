import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
from src.agent import NvidiaGemmaController

# Test with nemotron
ctl = NvidiaGemmaController(model="nvidia/nemotron-3.5-lightning-30b-a3b", max_tokens=512)

q = "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo nào và bởi ai?"
print(f"Testing Question: {q}")

t0 = time.time()
action1 = ctl.decide(q, history=[])
print(f"Step 1 ({time.time()-t0:.2f}s): {action1}")

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
print(f"Step 2 ({time.time()-t1:.2f}s): {action2}")
