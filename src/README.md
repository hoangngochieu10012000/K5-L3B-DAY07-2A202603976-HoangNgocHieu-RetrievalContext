# Hệ thống Agentic RAG — Day 7

Thư mục `src/` chứa toàn bộ mã nguồn triển khai Agentic RAG và các phương pháp truy xuất ngữ cảnh (Retrieval & Context Engineering).

## Cấu trúc mã nguồn

- `src/embeddings.py`: Adapter kết nối mô hình embedding `google/embeddinggemma-2` (768 chiều), tương thích với vector store Day 6.
- `src/bm25.py`: Hiện thực thuật toán Lexical Retrieval BM25Okapi với tiền xử lý và tách từ tiếng Việt.
- `src/retrievers.py`: Triển khai 4 phương pháp retrieval:
  1. `DenseRetriever`: Truy vấn vector trên Qdrant Local (`chunks_strategy_b`).
  2. `BM25Retriever`: Truy vấn từ khóa theo BM25Okapi.
  3. `HybridRetriever`: Hợp nhất Dense và BM25 qua thuật toán Reciprocal Rank Fusion (RRF $k=60$).
  4. `QueryTransformHybridRetriever`: Mở rộng từ khóa kỹ thuật kết hợp Hybrid RRF.
- `src/pipeline.py`: Pipeline đo đạc, so sánh hiệu năng các phương pháp retrieval trên split Dev và Test.
- `src/agent.py`: Agent Controller kết nối mô hình ngôn ngữ lớn `nvidia/nemotron-3.5-lightning-30b-a3b` qua NVIDIA NIM API (`https://integrate.api.nvidia.com/v1`).
- `src/agent_eval.py`: Điều phối đánh giá Agent trên toàn bộ 24 câu hỏi benchmark, hỗ trợ trích xuất citation, context budget, tính điểm grounded answer (0/1/2) và abstention.

## Hướng dẫn chạy thử nghiệm

1. **Chuẩn bị môi trường & API Key:**
   Điền API Key của bạn vào file `.env`:
   ```env
   NVIDIA_API_KEY=nvapi-...
   LLM_BASE_URL=https://integrate.api.nvidia.com/v1
   LLM_MODEL=nvidia/nemotron-3.5-lightning-30b-a3b
   ```

2. **Chạy kiểm thử unit tests:**
   ```bash
   python -m unittest discover -s tests -v
   ```

3. **Chạy so sánh các phương pháp Retrieval trên Dev và Test:**
   ```bash
   python -m src.pipeline
   ```

4. **Chạy benchmark đánh giá toàn diện Agent:**
   ```bash
   python -m src.agent_eval --split both --retriever hybrid
   ```
