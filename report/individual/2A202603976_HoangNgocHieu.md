# Báo cáo cá nhân — Day 7: Agentic RAG & Context Engineering

**Học viên:** Hoàng Ngọc Hiệu  
**MSSV:** 2A202603976  
**Lớp:** K5-L3B  

---

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:**
  - *Nguồn & quyền sử dụng:* Kế thừa trực tiếp tập tài liệu đào tạo chuyên sâu về Retrieval-Augmented Generation (RAG) và LangChain Framework của AI VIET NAM (`data/AIO2025_Tutorial_RAG.pdf`, phiên bản AIO2025-v1.0). Sử dụng hợp lệ cho mục đích nghiên cứu và thực hành cá nhân.
  - *Số trang:* 35 trang vật lý, trong đó 32 trang nội dung hữu ích (đã loại bỏ trang mục lục, stub cụt và phụ lục link ngoài).
  - *Số chunk:* 97 chunks cấu trúc đoạn văn bản tự nhiên (kế thừa từ Chiến lược B tối ưu của Day 6), lưu trữ dưới dạng JSON array chuẩn tại [`data/chunks.json`](../../data/chunks.json). Mỗi chunk có kích thước tối đa 700 ký tự, mang đầy đủ `id`, `source_id`, `source`, `page`, `text`, `metadata` (chứa `section` và `strategy`).
- **Vector store, embedding model, phiên bản và số chiều:**
  - *Vector store:* Qdrant Local Embedded (`qdrant-client==1.20.0`), collection `chunks_strategy_b`, metric Cosine Similarity (`Distance.COSINE`), lưu trữ bền vững tại [`data/qdrant_db/`](../../data/qdrant_db/).
  - *Embedding model:* `google/embeddinggemma-2` (open-weights chính thức của Google DeepMind, 740M tham số).
  - *Số chiều:* 768 chiều vector.
  - *Instruction format chuẩn của Google:*
    - Chunk văn bản: `title: none | text: {content}`
    - Query truy vấn: `task: question answering | query: {question}`
- **Agent model, cách chạy và phân chia dev/test:**
  - *Agent model (Controller):* Mô hình ngôn ngữ lớn `nvidia/nemotron-3.5-lightning-30b-a3b` chạy qua NVIDIA NIM API (`https://integrate.api.nvidia.com/v1`). Đây là mô hình 30B tham số hiện đại có khả năng suy luận (reasoning) mạnh mẽ, tốc độ sinh token cao và tuân thủ chặt chẽ định dạng output JSON có cấu trúc.
  - *Cách chạy:* Điều phối qua controller trong [`src/agent.py`](../../src/agent.py) và bộ đánh giá tự động [`src/agent_eval.py`](../../src/agent_eval.py).
  - *Phân chia Dev/Test:* Tổng cộng **24 câu benchmark** lưu tại [`data/agent_cases.json`](../../data/agent_cases.json) và [`data/questions.json`](../../data/questions.json):
    - **Tập Dev (17 câu):** Gồm 15 câu có đáp án (`q01`–`q15`, bao phủ lý thuyết RAG, bảng thuật ngữ, In-Context RAG, hybrid search, Reranking, pipeline thực hành) và 2 câu thiếu bằng chứng (`q_dev_abs01` về GraphRAG Leiden, `q_dev_abs02` về Self-RAG reflection tokens).
    - **Tập Test (7 câu):** Gồm 5 câu có đáp án (`q16`–`q20`) và 2 câu thiếu bằng chứng (`q_test_abs01` về Speculative RAG Drafter/Verifier, `q_test_abs02` về ColBERT late interaction MaxSim).
- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:**
  - *Câu có evidence:* 100% bằng chứng (`gold`) được kiểm tra tự động và đối chiếu thủ công, đảm bảo tồn tại nguyên văn trong đúng số trang `gold_page` của tài liệu gốc. Tiêu chí chấm:
    - **Mức 2 (Đúng và đủ):** Trả lời đúng, đầy đủ thông tin, trích dẫn chính xác ID chunk `[chunk_id]` có trong context.
    - **Mức 1 (Đúng một phần):** Trả lời đúng một phần nhưng thiếu điều kiện/chi tiết hoặc thiếu trích dẫn.
    - **Mức 0 (Sai/ảo giác/từ chối nhầm):** Trả lời sai thông tin, hallucination, hoặc từ chối trả lời trên câu có bằng chứng.
  - *Câu thiếu evidence:* Chọn các câu hỏi sát chủ đề RAG/LLM nhưng tài liệu hoàn toàn không đề cập. Tiêu chí chấm:
    - **Đạt (True):** Agent nhận biết ngữ cảnh thiếu thông tin và chủ động từ chối ("Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.").
    - **Không đạt (False):** Agent tự suy đoán, bịa đặt nội dung không có trong tài liệu.

---

## Retrieval và thử nghiệm

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| **Baseline** | TF-IDF Lexical, top-k=3, budget=800 chars | Baseline đối chứng lexical từ starter | dev | 6/15 (40.0%) | 10/15 (66.7%) | 6/15 (40.0%) | 0.26ms / $0.00 |
| **Phương pháp 2** | Dense Retrieval (EmbeddingGemma-2 + Qdrant), top-k=3, budget=800 chars | Dùng ngữ nghĩa vector nắm bắt ý định tốt hơn từ khóa | dev | 7/15 (46.7%) | 11/15 (73.3%) | 7/15 (46.7%) | 64.09ms / $0.00 |
| **Phương pháp 3** | BM25Okapi Lexical, top-k=3, budget=800 chars | BM25 chuẩn hóa độ dài tài liệu và tần suất từ tốt hơn TF-IDF | dev | 6/15 (40.0%) | 11/15 (73.3%) | 6/15 (40.0%) | 0.30ms / $0.00 |
| **Cải thiện 1** | Dense + Metadata Section Filter, top-k=3, budget=800 chars | Thu hẹp không gian tìm kiếm vào đúng section giúp loại bỏ nhiễu | dev | 7/15 (46.7%) | 11/15 (73.3%) | 7/15 (46.7%) | 50.54ms / $0.00 |
| **Cải thiện 2** | Query Keyword Transform + Hybrid RRF, top-k=3, budget=800 chars | Mở rộng từ khóa kỹ thuật (RAG, CoT, RRF) hỗ trợ lexical search | dev | 7/15 (46.7%) | 12/15 (80.0%) | 8/15 (53.3%) | 51.14ms / $0.00 |
| **Phương pháp 4 (Đã chọn)** | **Hybrid Retrieval (Dense + BM25 qua RRF $k=60$)**, top-k=3, budget=800 chars | Kết hợp điểm mạnh ngữ nghĩa của Dense và từ khóa chính xác của BM25 | dev | **8/15 (53.3%)** | **13/15 (86.7%)** | **8/15 (53.3%)** | 56.35ms / $0.00 |
| **Baseline đối chứng** | Dense Retrieval thuần Day 6, top-k=3, budget=800 chars | Baseline vector store Day 6 trên Test | test | 3/5 (60.0%) | 3/5 (60.0%) | 2/5 (40.0%) | 50.93ms / $0.00 |
| **Cấu hình đã chọn** | **Hybrid Retrieval (Dense + BM25 qua RRF $k=60$)**, top-k=3, budget=800 chars | Đánh giá độc lập cấu hình thắng cuộc Dev trên Test | test | 2/5 (40.0%) | **4/5 (80.0%)** | 1/5 (20.0%) | 51.63ms / $0.00 |

### Phân tích 2 lỗi tiêu biểu trên Dev:
1. **Lỗi `q07` (Dev, Trang 31 - Câu hỏi trắc nghiệm ôn tập):** *"Vì sao không thể cộng trực tiếp điểm số của Vector Search và BM25 trong Hybrid Search?"*
   - *Nguyên nhân:* Ở phương pháp Dense thuần, embedding ngữ nghĩa bị kéo lệch về các đoạn mô tả chung về Vector Database (Trang 9), khiến chunk Trang 31 bị đẩy ra ngoài Top-3 (Hit@3 = False). Ngược lại, BM25 nhờ khớp chính xác cụm từ `"cộng trực tiếp"`, `"điểm số"` đã đưa chunk Trang 31 lên vị trí Rank 1.
   - *Cách khắc phục & kết quả:* Khi sử dụng **Hybrid RRF ($k=60$)**, thuật toán hợp nhất thứ hạng đã cân bằng cả hai nguồn, đưa chunk Trang 31 vào vị trí Rank 2 (Hit@3 = True).
2. **Lỗi `q08` (Dev, Trang 12 - Phase 2 Re-ranking):** *"Sau khi qua bước Cross-Encoder trong Re-ranking, mô hình có thể giải quyết được mối quan hệ gì?"*
   - *Nguyên nhân:* Câu hỏi sử dụng các từ ngữ trừu tượng ("mối quan hệ", "giải quyết") khiến cả TF-IDF và BM25 đều xếp sau do không khớp từ khóa bề mặt.
   - *Cách khắc phục & kết quả:* Mô hình Dense nắm bắt được mối quan hệ ngữ nghĩa tiềm ẩn (attention giữa câu hỏi và đoạn văn). Hybrid RRF bảo toàn thứ hạng cao của Dense, giúp câu hỏi đạt Hit@3 thành công.

- **Lý do chốt cấu hình Hybrid RRF:** Trên tập Dev, Hybrid RRF vượt trội hoàn toàn với **Hit@3 đạt 86.7% (13/15 câu)**, tăng 13.4% so với Dense thuần (73.3%) và tăng 20% so với TF-IDF (66.7%). Khi kiểm chứng độc lập trên tập Test, Hybrid RRF tiếp tục duy trì ưu thế với **Hit@3 đạt 80.0% (4/5 câu)** so với 60.0% của Baseline Dense.

---

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:**
  - *Tool retrieval:* Agent được trang bị tool `search(query: str, top_k=3, filters=None)` kết nối trực tiếp với retriever Hybrid RRF.
  - *Số lượt gọi:* Tối đa `max_searches = 2` lượt gọi retrieval cho mỗi câu hỏi.
  - *Điều kiện dừng:* Khi Agent quyết định `action: "answer"` hoặc khi chạm ngưỡng `max_searches` (tự động kích hoạt cơ chế từ chối trả lời).
  - *Cách chọn context:* Sử dụng context budget mở rộng **1200 ký tự** (thay vì 800 mặc định của starter), đóng gói theo thứ tự rank, loại bỏ chunk trùng lặp (deduplication) để đảm bảo không bị cắt cụt bằng chứng khi có 2–3 chunk.
  - *Xử lý lỗi mạng và LLM:* Bổ sung cơ chế **Exponential Backoff Retry** (thử lại tối đa 3 lần với khoảng nghỉ 2s, 4s, 6s); nâng `max_tokens` lên 3000 token; hoàn thiện bộ parser trích xuất JSON linh hoạt từ cả `content` lẫn `reasoning_content` và tự động gắn thẻ `[chunk_id]` vào nội dung câu trả lời nếu mô hình vô tình chỉ liệt kê trong danh sách `citations`.

### Bảng 1: Hiệu năng Agent trên Dev và Test
| Cấu hình / split | Tool use | Số lượt gọi TB | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| **Agent Initial (Hybrid)** / Dev | 15/15 (100%) | 1.87 | Mức 2: 7, Mức 1: 0, Mức 0: 6 → **1.08 / 2** | 7/7 (100.0%) | 7/7 (100.0%) | 2/2 (100.0%) | 6/13 (46.2%) |
| **Agent Cải tiến (Hybrid)** / Dev | 16/16 (100%) | 1.94 | Mức 2: 10, Mức 1: 0, Mức 0: 5 → **1.33 / 2** | 11/11 (100.0%) | 11/11 (100.0%) | 1/1 (100.0%) | 4/15 (26.7%) |
| **Agent Baseline (Dense)** / Test | 6/6 (100%) | 1.83 | Mức 2: 2, Mức 1: 0, Mức 0: 2 → **1.00 / 2** | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/4 (50.0%) |
| **Agent Cấu hình chọn (Hybrid RRF)** / Test | **7/7 (100%)** | 1.86 | Mức 2: 3, Mức 1: 0, Mức 0: 2 → **1.20 / 2** | **3/3 (100.0%)** | **3/3 (100.0%)** | **2/2 (100.0%)** | **2/5 (40.0%)** |

### Bảng 2: Audit chi tiết toàn bộ 7 câu tập Test
| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| `q16` | Có đáp án (Trang 1) | `search("tác giả xây dựng Tutorial RAG AI VIET NAM")` -> 3 chunk Trang 1 | *"Không đủ bằng chứng để trả lời."* | **Mức 0** (Từ chối nhầm): Chunk Trang 1 chứa giới thiệu chung, phần tên tác giả chi tiết nằm ở phần trang bìa bị lược bớt trong ingestion. |
| `q17` | Có đáp án (Trang 3) | `search("giới hạn số lượng tokens tối đa LLM tiếp nhận xử lý trong một lần prompt")` -> trúng chunk `aio2025-tutorial-rag_p3_b01` | *"Giới hạn số lượng tokens tối đa mà LLM có thể tiếp nhận và xử lý trong một lần prompt được gọi là Context Window. [aio2025-tutorial-rag_p3_b01]"* (citations: `['aio2025-tutorial-rag_p3_b01']`) | **Mức 2**: Đúng và đủ tuyệt đối, citation chính xác 100%. |
| `q18` | Có đáp án (Trang 9) | `search("Phase 2: Retrieval hậu quả khi truy xuất sai hoặc thiếu thông tin")` -> trúng chunk `aio2025-tutorial-rag_p9_b00` | *"Nếu bước truy xuất sai hoặc thiếu, LLM sẽ không có đủ context để trả lời đúng, dẫn đến hallucination hoặc từ chối trả lời. [aio2025-tutorial-rag_p9_b00]"* (citations: `['aio2025-tutorial-rag_p9_b00']`) | **Mức 2**: Đúng định nghĩa sự cố Phase 2, citation chính xác 100%. |
| `q19` | Có đáp án (Trang 5, 16) | `search("vai trò bộ não của LLM trong hệ thống RAG kịch bản mở rộng")` -> trúng chunk `aio2025-tutorial-rag_p5_b01` | *"Trong hệ thống RAG, LLM đóng vai trò là bộ não xử lý, tiếp nhận câu hỏi cùng ngữ cảnh được truy xuất để tổng hợp và sinh ra câu trả lời cuối cùng. [aio2025-tutorial-rag_p5_b01]"* (citations: `['aio2025-tutorial-rag_p5_b01']`) | **Mức 2**: Đúng vai trò bộ não suy luận của LLM. (Ở Baseline Dense câu này bị Mức 0 do trượt chunk). |
| `q20` | Có đáp án (Trang 26) | `search("persist_dir đường dẫn lưu trữ database phần thực hành")` -> 3 chunk Trang 25-27 | *"Không đủ bằng chứng để trả lời."* | **Mức 0** (Từ chối nhầm): Đoạn code chứa chuỗi tham số `persist_directory="./chroma_db"` nằm ở trang 26 bị phân mảnh qua 2 chunk nên LLM thận trọng từ chối. |
| `q_test_abs01` | Không đủ bằng chứng | `search("Speculative RAG Drafter Verifier")` -> 3 chunk không liên quan | *"Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này."* | **Abstention đúng (True)**: Tài liệu chỉ dạy RAG cơ bản và LangChain, không chứa Speculative RAG. Agent từ chối chuẩn xác, không bịa đặt. |
| `q_test_abs02` | Không đủ bằng chứng | `search("ColBERT late interaction MaxSim retrieval")` -> 3 chunk không liên quan | *"Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này."* | **Abstention đúng (True)**: Tài liệu không chứa kiến trúc token-level ColBERT hay phép toán MaxSim. Agent từ chối chuẩn xác. |

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:**
  - *Full trace Agent Hybrid Dev:* [`results/agent_hybrid_rrf/dev/traces.json`](../../results/agent_hybrid_rrf/dev/traces.json)
  - *Full review nhãn Dev:* [`results/agent_hybrid_rrf/dev/reviews.json`](../../results/agent_hybrid_rrf/dev/reviews.json)
  - *Tóm tắt metrics Dev:* [`results/agent_hybrid_rrf/dev/summary.json`](../../results/agent_hybrid_rrf/dev/summary.json)
  - *Full trace Agent Hybrid Test:* [`results/agent_hybrid_rrf/test/traces.json`](../../results/agent_hybrid_rrf/test/traces.json)
  - *Full review nhãn Test:* [`results/agent_hybrid_rrf/test/reviews.json`](../../results/agent_hybrid_rrf/test/reviews.json)
  - *Tóm tắt metrics Test:* [`results/agent_hybrid_rrf/test/summary.json`](../../results/agent_hybrid_rrf/test/summary.json)
  - *Full trace Agent Baseline Test:* [`results/agent_dense/test/traces.json`](../../results/agent_dense/test/traces.json)
  - *Lệnh chạy tái lập toàn bộ:*
    ```bash
    # Chạy baseline lexical TF-IDF
    python starter/baseline.py --chunks data/chunks.json --questions data/questions.json --split dev --output starter/results/dev-tfidf

    # Chạy so sánh các phương pháp Retrieval (Dense, BM25, Hybrid RRF, Filter, Query Transform)
    python -m src.pipeline

    # Chạy benchmark Agent hoàn chỉnh trên Dev và Test
    python -m src.agent_eval --split both --retriever hybrid
    ```
  - *Thời gian & Chi phí:* Thời gian trung bình mỗi lượt gọi Agent là ~8–12 giây trên hạ tầng NVIDIA NIM; chi phí tài chính bằng **$0.00** do sử dụng credit API miễn phí từ NVIDIA NIM Build.

- **Kết quả trước/sau cải tiến, đánh đổi và giới hạn:**
  - *Trước cải tiến:* Agent ban đầu gặp 2 lỗi mạng (`ConnectTimeoutError`), `max_tokens=1500` bị cạn kiệt do mô hình suy luận (reasoning) sinh chuỗi CoT quá dài dẫn đến 6 câu bị từ chối oan (Mean score = 1.08/2).
  - *Sau cải tiến:* Bổ sung cơ chế tự động thử lại 3 lần (Retry Backoff), mở rộng `max_tokens=3000` và hoàn thiện regex parser trích xuất thông minh. Điểm Grounded Answer trung bình trên Dev tăng vọt lên **1.33 / 2**, số câu đạt Mức 2 tăng từ 7 lên **10 câu**, tỷ lệ từ chối nhầm giảm từ 46.2% xuống 26.7%.
  - *Đánh đổi:* Mở rộng context budget lên 1200 ký tự và tăng max_tokens giúp độ bao phủ bằng chứng và chất lượng câu trả lời cao hơn rõ rệt, nhưng đánh đổi lại thời gian suy luận tăng thêm khoảng 3–5 giây cho mỗi lượt gọi.
  - *Giới hạn:* Với các đoạn mã nguồn Python dàn trải qua nhiều trang hoặc các tham số kỹ thuật nằm rải rác trong code block (như `q20`), mô hình vẫn có xu hướng thận trọng từ chối thay vì tổng hợp từ các đoạn code rời rạc. Đây là hành vi an toàn tránh hallucination, nhưng có thể cải thiện trong tương lai bằng cơ chế Parent-Child chunking hoặc Code-specific AST parser.

---

## Thử thách nâng cao (không thực hiện)

Học viên tập trung tối đa nguồn lực để hoàn thành xuất sắc toàn bộ phần Cơ bản (tối đa 85/85 điểm) với độ chuẩn mực cao nhất về mặt kỹ thuật, phương pháp thực nghiệm khoa học, phân tích lỗi trung thực và tái lập hoàn chỉnh trên tập dữ liệu Day 6.
