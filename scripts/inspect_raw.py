import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import NvidiaGemmaController

ctl = NvidiaGemmaController()
q = "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo nào và bởi ai?"

dummy_context = (
    "[aio2025-tutorial-rag_p4_b00 | data/AIO2025_Tutorial_RAG.pdf | page 4]\n"
    "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo khoa học “Retrieval-\n"
    "Augmented Generation for Knowledge-Intensive NLP Tasks” bởi Patrick Lewis và các cộng\n"
    "sự tại Facebook AI Research (FAIR) vào năm 2020."
)
history = [{
    "tool": "search",
    "queries": ["first Retrieval-Augmented Generation paper"],
    "context": dummy_context,
    "context_ids": ["aio2025-tutorial-rag_p4_b00"]
}]

# Check raw LLM output
system_prompt = (
    "Bạn là một trợ lý AI thông minh chuyên nghiên cứu tài liệu kỹ thuật về RAG và LangChain.\n"
    "Chỉ trả về JSON duy nhất: {\"action\": \"answer\", \"answer\": \"... [chunk_id]\", \"citations\": [\"chunk_id\"]}"
)
user_content = f"Câu hỏi: {q}\nNgữ cảnh:\n{dummy_context}\n\nTrả lời dựa trên ngữ cảnh và trích dẫn [chunk_id]."

raw = ctl._call_llm([
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_content}
])
print("RAW OUTPUT LENGTH:", len(raw))
print("RAW OUTPUT:")
print(raw)
