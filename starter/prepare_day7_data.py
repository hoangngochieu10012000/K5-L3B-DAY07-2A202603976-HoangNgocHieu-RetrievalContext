"""Prepare Day 7 data from Day 6 Qdrant vector store and benchmark questions."""
import json
import re
import sys
import unicodedata
from pathlib import Path
from qdrant_client import QdrantClient

# Add starter to path
sys.path.append(str(Path(__file__).parent))
from baseline import validate, hit


def normalize_words(text: str) -> list[str]:
    return unicodedata.normalize('NFC', text).split()


def find_exact_substring(chunk_text: str, evidence_quote: str) -> str | None:
    """Find the exact substring in chunk_text that matches evidence_quote ignoring whitespace variations."""
    if evidence_quote in chunk_text:
        return evidence_quote

    ev_words = normalize_words(evidence_quote)
    if not ev_words:
        return None

    # Search by words sequence in chunk_text
    # Escape words for regex and join with \s+
    pattern = r'\s+'.join(re.escape(w) for w in ev_words)
    match = re.search(pattern, chunk_text)
    if match:
        return match.group(0)

    # If full match fails, try 80% prefix
    if len(ev_words) > 5:
        sub_words = ev_words[: int(len(ev_words) * 0.8)]
        sub_pattern = r'\s+'.join(re.escape(w) for w in sub_words)
        match = re.search(sub_pattern, chunk_text)
        if match:
            return match.group(0)

    return None


def main():
    qdrant_path = Path("data/qdrant_db")
    if not qdrant_path.exists():
        raise FileNotFoundError(f"Qdrant path not found at {qdrant_path}")

    print("Loading chunks from Qdrant chunks_strategy_b...")
    client = QdrantClient(path=str(qdrant_path))
    points, _ = client.scroll(collection_name="chunks_strategy_b", limit=300, with_payload=True)
    client.close()

    chunks = []
    chunks_by_page = {}
    for p in points:
        pl = p.payload
        c = {
            "id": pl["chunk_id"],
            "source_id": pl["document_id"],
            "source": "data/AIO2025_Tutorial_RAG.pdf",
            "page": int(pl["page"]),
            "text": pl["text"],
            "metadata": pl.get("metadata", {}),
        }
        if "section" in pl and "section" not in c["metadata"]:
            c["metadata"]["section"] = pl["section"]
        chunks.append(c)
        chunks_by_page.setdefault(c["page"], []).append(c)

    print(f"Loaded {len(chunks)} chunks.")

    # Load Day 6 questions
    day6_benchmark_path = Path("D:/AI20K/Lab06/K5-L3B-DAY06-HoangNgocHieu-2A202603976-DataIngestion/starter/data/benchmark.json")
    if not day6_benchmark_path.exists():
        raise FileNotFoundError(f"Day 6 benchmark not found at {day6_benchmark_path}")

    with open(day6_benchmark_path, "r", encoding="utf-8") as f:
        raw_questions = json.load(f)

    questions = []
    agent_cases = []

    for q in raw_questions:
        qid = q["id"]
        split = q["split"]
        page = q["gold_page"]
        if isinstance(page, list):
            page = page[0]
        ev_quote = q["evidence_quote"]
        if isinstance(ev_quote, list):
            ev_quote = ev_quote[0]

        matching_chunks = chunks_by_page.get(page, [])
        exact_sub = None
        matched_chunk_id = None
        for c in matching_chunks:
            exact_sub = find_exact_substring(c["text"], ev_quote)
            if exact_sub:
                matched_chunk_id = c["id"]
                break

        if not exact_sub:
            raise ValueError(f"Could not find exact evidence substring for {qid} on page {page}")

        gold = [{
            "source_id": "aio2025-tutorial-rag",
            "page": page,
            "evidence": exact_sub
        }]

        item = {
            "id": qid,
            "split": split,
            "question": q["question"],
            "gold": gold,
            "expected_answer": q["expected_answer"]
        }
        if q.get("filter"):
            item["filter"] = q["filter"]

        questions.append(item)

        agent_cases.append({
            "id": qid,
            "split": split,
            "question": q["question"],
            "answerable": True,
            "expected_behavior": "search_and_answer",
            "target_chunk_id": matched_chunk_id
        })

    # Add abstention questions
    abstention_specs = [
        {
            "id": "q_dev_abs01",
            "split": "dev",
            "question": "Kiến trúc GraphRAG sử dụng thuật toán Leiden để phát hiện các cộng đồng mạng đồ thị tri thức như thế nào?",
            "answerable": False,
            "expected_behavior": "search_and_abstain",
            "absence_reason": "Tài liệu AIO2025 RAG Tutorial chỉ đề cập đến RAG cơ bản, In-Context RAG và LangChain, không chứa thông tin về GraphRAG hay thuật toán phân cụm Leiden."
        },
        {
            "id": "q_dev_abs02",
            "split": "dev",
            "question": "Hệ thống Self-RAG sử dụng các reflection tokens nào để kiểm soát quá trình truy xuất và tự sửa lỗi câu trả lời?",
            "answerable": False,
            "expected_behavior": "search_and_abstain",
            "absence_reason": "Tài liệu chỉ thảo luận về In-Context RAG với Generator thông thường, hoàn toàn không nhắc đến kỹ thuật Self-RAG hay các reflection tokens."
        },
        {
            "id": "q_test_abs01",
            "split": "test",
            "question": "Cơ chế Speculative RAG sử dụng mô hình nhỏ (Drafter) để tạo dự đoán trước khi chuyển cho Verifier như thế nào?",
            "answerable": False,
            "expected_behavior": "search_and_abstain",
            "absence_reason": "Tài liệu không đề cập đến kiến trúc Speculative RAG hay mô hình Drafter/Verifier."
        },
        {
            "id": "q_test_abs02",
            "split": "test",
            "question": "Mô hình ColBERT áp dụng cơ chế late interaction với phép toán MaxSim cụ thể ra sao trong bước retrieval?",
            "answerable": False,
            "expected_behavior": "search_and_abstain",
            "absence_reason": "Tài liệu chỉ giới thiệu dense retrieval (cosine/dot product), TF-IDF/BM25 và Hybrid search thông thường, không chứa kiến trúc token-level late interaction của ColBERT hay MaxSim."
        }
    ]

    for abs_case in abstention_specs:
        agent_cases.append(abs_case)

    # Validate answerable questions with baseline validate()
    print("Validating Dev questions...")
    dev_q = [q for q in questions if q["split"] == "dev"]
    validate(chunks, dev_q)
    print(f"Dev questions valid ({len(dev_q)} questions).")

    print("Validating Test questions...")
    test_q = [q for q in questions if q["split"] == "test"]
    validate(chunks, test_q)
    print(f"Test questions valid ({len(test_q)} questions).")

    # Save to data directory
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)

    with open(out_dir / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    with open(out_dir / "questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    with open(out_dir / "agent_cases.json", "w", encoding="utf-8") as f:
        json.dump(agent_cases, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated:")
    print(f" - {out_dir / 'chunks.json'} ({len(chunks)} chunks)")
    print(f" - {out_dir / 'questions.json'} ({len(questions)} answerable questions: {len(dev_q)} dev, {len(test_q)} test)")
    print(f" - {out_dir / 'agent_cases.json'} ({len(agent_cases)} total cases: {len(agent_cases) - len(abstention_specs)} answerable, {len(abstention_specs)} abstention)")


if __name__ == "__main__":
    main()
