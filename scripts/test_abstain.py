import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import NvidiaGemmaController

ctl = NvidiaGemmaController()
q = "Kiến trúc GraphRAG sử dụng thuật toán Leiden để phát hiện các cộng đồng mạng đồ thị tri thức như thế nào?"
print(f"Testing Abstention Question: {q}")

# Step 1: Decision on empty context
action1 = ctl.decide(q, history=[])
print(f"Step 1 Action: {action1}")

# Step 2: Context retrieved has no info on GraphRAG or Leiden
irrelevant_context = (
    "[aio2025-tutorial-rag_p4_b00 | page 4]\n"
    "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo khoa học “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks” vào năm 2020."
)
history = [{
    "tool": "search",
    "queries": [action1.get("query", q)],
    "context": irrelevant_context,
    "context_ids": ["aio2025-tutorial-rag_p4_b00"]
}]

action2 = ctl.decide(q, history=history)
print(f"Step 2 Action: {action2}")
