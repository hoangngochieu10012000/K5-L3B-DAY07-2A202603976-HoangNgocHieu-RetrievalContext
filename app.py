"""Streamlit Demo Application for Day 07: Agentic RAG & Context Engineering.
Học viên: Hoàng Ngọc Hiệu - MSSV: 2A202603976 - Lớp: K5-L3B
Hỗ trợ cả 2 bài toán: Phần Cơ Bản (AIO2025 RAG) và Thử Thách Nâng Cao Bonus (SGK Địa lí 10 - KNTT).
"""
import os
import sys
import json
import time
from pathlib import Path
from typing import Any

import streamlit as st
import pandas as pd

# Set working directory and sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "starter") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "starter"))

from starter.baseline import pack_context
from starter.agentic import run_agent
from src.embeddings import Day6Embedder
from src.retrievers import DenseRetriever, BM25Retriever, HybridRetriever, QueryTransformHybridRetriever
from src.agent import NvidiaGemmaController, load_env_file

# Streamlit Page Config
st.set_page_config(
    page_title="Day 07: Agentic RAG Demo - Hoang Ngoc Hieu",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.02rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .metric-box {
        background: #F3F4F6;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1D4ED8;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6B7280;
    }
    .badge-success {
        display: inline-block;
        background-color: #DEF7EC;
        color: #03543F;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .badge-warning {
        display: inline-block;
        background-color: #FEF08A;
        color: #713F12;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .badge-info {
        display: inline-block;
        background-color: #E0E7FF;
        color: #3730A3;
        font-size: 0.85rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .chunk-card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# Adapter for starter run_agent protocol
class AgentRetrieverAdapter:
    def __init__(self, retriever):
        self.retriever = retriever

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        return self.retriever.search(query, top_k=top_k, filters=filters)


# ---------------- Caching Resources ----------------
@st.cache_resource(show_spinner="Đang nạp tập dữ liệu...")
def load_dataset(dataset_key: str):
    if dataset_key == "bonus":
        chunks_path = ROOT_DIR / "data" / "bonus" / "chunks.json"
        questions_path = ROOT_DIR / "data" / "bonus" / "questions.json"
        cases_path = ROOT_DIR / "data" / "bonus" / "agent_cases.json"
    else:
        chunks_path = ROOT_DIR / "data" / "chunks.json"
        questions_path = ROOT_DIR / "data" / "questions.json"
        cases_path = ROOT_DIR / "data" / "agent_cases.json"

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    with open(questions_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    with open(cases_path, "r", encoding="utf-8") as f:
        agent_cases = json.load(f)

    return chunks, questions, agent_cases


@st.cache_resource(show_spinner="Đang khởi tạo các mô hình Retrieval (EmbeddingGemma-2, Qdrant, BM25)...")
def load_retrieval_system(dataset_key: str):
    chunks, _, _ = load_dataset(dataset_key)
    embedder = Day6Embedder()
    coll_name = "bonus_sgk10" if dataset_key == "bonus" else "chunks_strategy_b"
    dense = DenseRetriever(qdrant_path="data/qdrant_db", collection_name=coll_name, embedder=embedder)
    bm25 = BM25Retriever(chunks)
    hybrid = HybridRetriever(dense, bm25, rrf_k=60)
    query_transform = QueryTransformHybridRetriever(hybrid)
    return {
        "embedder": embedder,
        "dense": dense,
        "bm25": bm25,
        "hybrid": hybrid,
        "query_transform": query_transform
    }


@st.cache_resource(show_spinner="Đang kết nối NVIDIA NIM API Controller...")
def load_controller():
    try:
        controller = NvidiaGemmaController()
        return controller, None
    except Exception as e:
        return None, str(e)


@st.cache_data
def load_benchmark_results(dataset_key: str):
    results = {}
    if dataset_key == "bonus":
        base_res = ROOT_DIR / "results" / "bonus"
        targets = {
            "dense_dev": base_res / "dense_dev" / "summary.json",
            "bm25_dev": base_res / "bm25_dev" / "summary.json",
            "hybrid_dev": base_res / "hybrid_rrf_dev" / "summary.json",
            "dense_test": base_res / "dense_test" / "summary.json",
            "bm25_test": base_res / "bm25_test" / "summary.json",
            "hybrid_test": base_res / "hybrid_rrf_test" / "summary.json",
            "agent_dev_summary": base_res / "agent_hybrid_dev" / "summary.json",
            "agent_dev_traces": base_res / "agent_hybrid_dev" / "traces.json",
            "agent_dev_reviews": base_res / "agent_hybrid_dev" / "reviews.json",
            "agent_test_summary": base_res / "agent_hybrid_test" / "summary.json",
            "agent_test_traces": base_res / "agent_hybrid_test" / "traces.json",
            "agent_test_reviews": base_res / "agent_hybrid_test" / "reviews.json",
        }
    else:
        base_res = ROOT_DIR / "results"
        targets = {
            "dense_dev": base_res / "method_dense_dev" / "summary.json",
            "bm25_dev": base_res / "method_bm25_dev" / "summary.json",
            "hybrid_dev": base_res / "method_hybrid_rrf_dev" / "summary.json",
            "dense_test": base_res / "baseline_dense_test" / "summary.json",
            "hybrid_test": base_res / "chosen_hybrid_rrf_test" / "summary.json",
            "agent_dev_summary": base_res / "agent_hybrid_rrf" / "dev" / "summary.json",
            "agent_dev_traces": base_res / "agent_hybrid_rrf" / "dev" / "traces.json",
            "agent_dev_reviews": base_res / "agent_hybrid_rrf" / "dev" / "reviews.json",
            "agent_test_summary": base_res / "agent_hybrid_rrf" / "test" / "summary.json",
            "agent_test_traces": base_res / "agent_hybrid_rrf" / "test" / "traces.json",
            "agent_test_reviews": base_res / "agent_hybrid_rrf" / "test" / "reviews.json",
        }
    for k, pth in targets.items():
        if pth.exists():
            try:
                with open(pth, "r", encoding="utf-8") as f:
                    results[k] = json.load(f)
            except Exception:
                pass
    return results


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/1024025?s=200&v=4", width=50)
    st.markdown("### 🎓 Khóa học AI VIET NAM — AI20K")
    st.markdown("**Day 07: Agentic RAG & Context Engineering**")
    st.markdown("---")

    st.markdown("#### 👤 Thông tin sinh viên")
    st.markdown("- **Học viên:** Hoàng Ngọc Hiệu")
    st.markdown("- **MSSV:** `2A202603976`")
    st.markdown("- **Lớp:** `K5-L3B`")
    st.markdown("---")

    st.markdown("#### 📂 Chọn Bộ Dữ Liệu & Bài Toán")
    dataset_option = st.selectbox(
        "Tập dữ liệu đang kiểm thử:",
        [
            "1. AIO2025 RAG Tutorial (Phần cơ bản)",
            "2. SGK Địa lí 10 - KNTT (Thử thách nâng cao - Bonus)"
        ],
        index=0
    )
    is_bonus = "Bonus" in dataset_option
    dataset_key = "bonus" if is_bonus else "base"

    st.markdown("---")
    st.markdown("#### ⚙️ Cấu hình Hệ Thống")
    top_k = st.slider("Top-K Retrieval", min_value=1, max_value=5, value=3, step=1)
    default_budget = 1500 if is_bonus else 1200
    budget = st.slider("Context Budget (chars)", min_value=600, max_value=2500, value=default_budget, step=100)
    default_max_searches = 3 if is_bonus else 2
    max_searches = st.slider("Max Search Calls", min_value=1, max_value=4, value=default_max_searches, step=1)
    rrf_k = st.number_input("RRF Constant (k)", min_value=10, max_value=120, value=60, step=5)
    st.markdown("---")

    # Load active data
    chunks, questions, agent_cases = load_dataset(dataset_key)
    case_map = {c["id"]: c for c in agent_cases}
    bench_results = load_benchmark_results(dataset_key)

    retrievers = None
    retrieval_err = None
    try:
        retrievers = load_retrieval_system(dataset_key)
    except Exception as e:
        retrieval_err = str(e)

    controller, controller_err = load_controller()

    st.markdown("#### 📡 Trạng thái Thành phần")
    if retrievers:
        coll_disp = "bonus_sgk10" if is_bonus else "chunks_strategy_b"
        st.success(f"✅ Qdrant Local: `{coll_disp}` ({len(chunks)} chunks, 768d)")
        st.success(f"✅ BM25: BM25Okapi ({len(chunks)} docs)")
    else:
        st.error(f"❌ Retrieval lỗi: {retrieval_err}")

    if controller:
        st.success(f"✅ LLM: `{controller.model}`")
    else:
        st.warning("⚠️ LLM NIM: Chưa kết nối (kiểm tra .env)")


# ---------------- MAIN APP HEADER ----------------
if is_bonus:
    st.markdown('<div class="main-title">🌍 SGK Địa lí 10: Multimodal Agentic RAG (Bonus Challenge)</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Ứng dụng Demo Thử thách nâng cao (118 trang tài liệu thực tế): '
        'Bóc tách đa phương thức (Bảng số liệu kinh tế, Sơ đồ tư duy, Bản đồ vận tải biển & hàng không thế giới), '
        'truy xuất Hybrid RRF và Agent suy luận trích dẫn đạt <b>96.67% độ chính xác</b> trên tập Test.</div>',
        unsafe_allow_html=True
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="metric-box"><div class="metric-value">32</div><div class="metric-label">Chunks Đa Phương Thức</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><div class="metric-value">118</div><div class="metric-label">Trang SGK Địa lí 10</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><div class="metric-value">100%</div><div class="metric-label">Hit@3 Test (Hybrid)</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><div class="metric-value">96.67%</div><div class="metric-label">Test Accuracy (29/30)</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-box"><div class="metric-value">+15 / 15</div><div class="metric-label">Điểm Thử Thách Bonus</div></div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="main-title">🤖 AIO2025: Agentic RAG & Context Engineering</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Ứng dụng Demo toàn diện Day 07: Khảo sát Ingestion Day 6, Thực nghiệm So sánh 4 Phương pháp Retrieval, '
        'và Trợ lý Agentic RAG hỏi đáp tự động với cơ chế Trích dẫn & Từ chối an toàn.</div>',
        unsafe_allow_html=True
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="metric-box"><div class="metric-value">97</div><div class="metric-label">Văn bản Chunks (B)</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><div class="metric-value">32</div><div class="metric-label">Trang Tài liệu PDF</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><div class="metric-value">768</div><div class="metric-label">Số chiều Embedding</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><div class="metric-value">86.7%</div><div class="metric-label">Hit@3 Dev (Hybrid)</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-box"><div class="metric-value">1.33 / 2</div><div class="metric-label">Điểm Agent Dev</div></div>', unsafe_allow_html=True)

st.write("")

# Main Tabs
audit_tab_title = f"📋 4. Audit Benchmark ({len(agent_cases)} Cases)"
tab_chat, tab_retrieval, tab_data, tab_audit, tab_report = st.tabs([
    "💬 1. Hỏi Đáp Agentic RAG",
    "🔍 2. So Sánh Retrieval",
    "📊 3. Dữ Liệu & Ingestion",
    audit_tab_title,
    "📈 5. Bảng Điểm & Báo Cáo"
])


# =========================================================================
# TAB 1: AGENTIC RAG CHAT & INTERACTION
# =========================================================================
with tab_chat:
    st.markdown("### 🤖 Trợ lý AI Hỏi Đáp Thông Minh (Agentic RAG Controller)")
    st.markdown(
        "Agent tự động phân tích câu hỏi của bạn, quyết định gọi tool `search` với từ khóa tối ưu, "
        "tổng hợp thông tin từ ngữ cảnh tài liệu và chèn ký hiệu trích dẫn `[chunk_id]`. "
        "Nếu câu hỏi nằm ngoài tài liệu, Agent sẽ **chủ động từ chối an toàn** để triệt tiêu Hallucination."
    )

    if is_bonus:
        with st.expander("🖼️ Xem 3 Nội Dung Phức Tạp (Sơ Đồ Tư Duy, Bảng Số Liệu, Bản Đồ Thế Giới) đã OCR & Trích Xuất", expanded=True):
            img_c1, img_c2, img_c3 = st.columns(3)
            with img_c1:
                p98_path = ROOT_DIR / "assets" / "bonus_images" / "sgk10_p98_mindmap_buuchinh.png"
                if p98_path.exists():
                    st.image(str(p98_path), caption="Trang 98: Sơ đồ tư duy Vai trò bưu chính viễn thông")
                st.caption("🔹 **Chunk:** `sgk10_p98_diagram_buuchinh` — Gồm 2 nhánh: Phát triển kinh tế & Các lĩnh vực khác.")
            with img_c2:
                p92_path = ROOT_DIR / "assets" / "bonus_images" / "sgk10_p92_table33_gdp.png"
                if p92_path.exists():
                    st.image(str(p92_path), caption="Trang 92: Bảng 33 Cơ cấu GDP thế giới theo ngành (2000 & 2019)")
                st.caption("🔹 **Chunk:** `sgk10_p92_table33_gdp` — Dịch vụ: 64,1% (2000) -> 67,9% (2019); CN: 30,7% -> 27,9%.")
            with img_c3:
                p96_path = ROOT_DIR / "assets" / "bonus_images" / "sgk10_p96_map_hangkhong_duongbien.png"
                if p96_path.exists():
                    st.image(str(p96_path), caption="Trang 96: Hình 34.6 Bản đồ mạng lưới đường biển & hàng không thế giới")
                st.caption("🔹 **Chunk:** `sgk10_p96_map_hangkhong_bien` — Các cảng biển: Thượng Hải, Rotterdam; Sân bay: Atlanta, Bắc Kinh, Dubai.")

    # Preset selector
    preset_options = ["--- Nhập câu hỏi tùy ý bên dưới ---"]
    for q in agent_cases:
        split_tag = "[Dev]" if q["split"] == "dev" else "[Test]"
        cat_tag = f"[{q.get('category', '').upper()}]"
        ans_tag = "✅" if q["answerable"] else "⚠️ Không evidence"
        preset_options.append(f"{q['id']} {split_tag} {cat_tag} {ans_tag} - {q['question']}")

    selected_preset = st.selectbox(
        f"🎯 Chọn câu hỏi mẫu từ bộ Benchmark ({len(agent_cases)} câu hỏi chuẩn):",
        options=preset_options,
        index=0
    )

    default_question = ""
    if selected_preset != "--- Nhập câu hỏi tùy ý bên dưới ---":
        qid = selected_preset.split(" ")[0]
        match_case = next((c for c in agent_cases if c["id"] == qid), None)
        if match_case:
            default_question = match_case["question"]

    placeholder_text = (
        "Ví dụ: Theo Bảng 33 (Trang 92), tỉ trọng của ngành Dịch vụ trong cơ cấu GDP thế giới năm 2019 là bao nhiêu?"
        if is_bonus else
        "Ví dụ: Khái niệm RAG lần đầu tiên được đề xuất trong bài báo nào và bởi ai?"
    )

    user_query = st.text_area(
        "Nhập câu hỏi của bạn:",
        value=default_question,
        placeholder=placeholder_text,
        height=85
    )

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        run_btn = st.button("🚀 Gửi tới Agent", type="primary", use_container_width=True)
    with col_btn2:
        use_precomputed = st.checkbox("Sử dụng bản ghi đánh giá chính thức (phản hồi tức thì với đầy đủ trace/citations)", value=True)

    if run_btn and user_query.strip():
        found_trace = None
        if use_precomputed:
            for split_name in ("agent_test_traces", "agent_dev_traces"):
                traces_list = bench_results.get(split_name, [])
                for tr in traces_list:
                    qid = tr.get("query_id")
                    case_info = case_map.get(qid, {})
                    case_q = case_info.get("question", "")
                    if (case_q and case_q.strip().lower() == user_query.strip().lower()) or qid == selected_preset.split(" ")[0]:
                        found_trace = (tr, case_info)
                        break
                if found_trace:
                    break

        if found_trace:
            tr, case_info = found_trace
            st.info(f"💡 Đang hiển thị kết quả ghi nhận từ lượt đánh giá chính thức ({case_info.get('id', '')} - Tập {case_info.get('split', '').upper()}):")
            status = tr.get("status", "answered")
            answer = tr.get("answer", "")
            citations = tr.get("citations", [])
            events = tr.get("events", [])

            if status == "answered":
                st.markdown('<span class="badge-success">🟢 TRẢ LỜI CÓ BẰNG CHỨNG (Answered)</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-warning">🟡 TỪ CHỐI AN TOÀN (Abstained - Không đủ bằng chứng)</span>', unsafe_allow_html=True)

            st.markdown(f"#### 📝 Câu trả lời của Agent:\n{answer}")

            if citations:
                st.markdown(f"**📌 Các Chunks được trích dẫn:** {', '.join(f'`[{c}]`' for c in citations)}")

            with st.expander("🔍 Chi tiết Quá trình Thực thi Tool (Execution Trace)", expanded=True):
                for idx, ev in enumerate(events, 1):
                    event_type = ev.get("event")
                    if event_type == "search":
                        st.markdown(f"**Lượt {idx}: Gọi Tool `search(query='{ev.get('query')}')`**")
                        st.markdown(f"- **Số chunk lấy về:** {len(ev.get('results', []))}")
                        st.markdown(f"- **Context IDs nạp vào context budget:** `{ev.get('context_ids', [])}`")
                        for r in ev.get("results", []):
                            st.caption(f"🔹 Chunk `[{r['id']}]` - Trang {r['page']} (RRF Score: {r['score']:.4f})")
                            st.text(r['text'][:250] + ("..." if len(r['text']) > 250 else ""))
                    elif event_type == "answer":
                        st.markdown(f"**Lượt {idx}: Agent tổng hợp câu trả lời cuối cùng kèm trích dẫn.**")
                    elif event_type in ("invalid_or_missing_citations", "search_limit"):
                        st.markdown(f"**Lượt {idx}: Từ chối vì thiếu trích dẫn hợp lệ hoặc không có bằng chứng.**")

        else:
            if not controller:
                st.error("❌ Không thể chạy Agent trực tiếp vì chưa cấu hình `NVIDIA_API_KEY` hợp lệ trong `.env`.")
                st.info("Vui lòng tích chọn 'Sử dụng bản ghi đánh giá chính thức' để xem ngay kết quả mẫu!")
            elif not retrievers:
                st.error(f"❌ Không thể nạp hệ thống retrieval: {retrieval_err}")
            else:
                with st.spinner("🤖 Agent đang suy luận và điều phối tìm kiếm trực tiếp..."):
                    adapter = AgentRetrieverAdapter(retrievers["hybrid"])
                    try:
                        start_time = time.perf_counter()
                        trace = run_agent(
                            question=user_query.strip(),
                            controller=controller,
                            retriever=adapter,
                            top_k=top_k,
                            budget=budget,
                            max_searches=max_searches
                        )
                        elapsed = time.perf_counter() - start_time

                        status = trace.get("status")
                        answer = trace.get("answer", "")
                        citations = trace.get("citations", [])
                        events = trace.get("events", [])

                        if status == "answered":
                            st.markdown(f'<span class="badge-success">🟢 TRẢ LỜI CÓ BẰNG CHỨNG ({elapsed:.2f}s)</span>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<span class="badge-warning">🟡 TỪ CHỐI AN TOÀN ({elapsed:.2f}s)</span>', unsafe_allow_html=True)

                        st.markdown(f"#### 📝 Câu trả lời của Agent:\n{answer}")

                        if citations:
                            st.markdown(f"**📌 Trích dẫn:** {', '.join(f'`[{c}]`' for c in citations)}")

                        with st.expander("🔍 Chi tiết Quá trình Gọi Tool Trực Tiếp", expanded=True):
                            for idx, ev in enumerate(events, 1):
                                if ev.get("event") == "search":
                                    st.markdown(f"**Lượt {idx}: Agent yêu cầu tìm kiếm `query='{ev.get('query')}'`**")
                                    st.markdown(f"- Chunks được chọn: `{ev.get('context_ids', [])}`")
                                    for r in ev.get("results", []):
                                        st.caption(f"🔹 `[{r['id']}]` - Trang {r['page']} (RRF: {r['score']:.4f})")
                                        st.text(r['text'][:300] + "...")
                                elif ev.get("event") == "answer":
                                    st.markdown(f"**Lượt {idx}: Hoàn thành câu trả lời.**")
                                else:
                                    st.markdown(f"**Sự kiện:** `{ev.get('event')}`")

                    except Exception as e:
                        st.error(f"Lỗi khi thực thi Agent: {e}")


# =========================================================================
# TAB 2: RETRIEVAL METHOD COMPARISON
# =========================================================================
with tab_retrieval:
    st.markdown("### 🔍 Thử Nghiệm & So Sánh Các Phương Pháp Retrieval")
    st.markdown(
        "So sánh trực quan kết quả truy xuất giữa các thuật toán: "
        "**Dense Retrieval** (Ngữ nghĩa vector), **BM25Okapi** (Khớp từ khóa tần suất), **Hybrid RRF** (Hợp nhất thứ hạng $k=60$) "
        "và **Query Transform Hybrid**."
    )

    col_q1, col_q2 = st.columns([3, 1])
    with col_q1:
        if is_bonus:
            sample_q_list = [
                "Theo Bảng 33 (Trang 92), tỉ trọng của ngành Dịch vụ trong cơ cấu GDP thế giới năm 2019 đạt bao nhiêu phần trăm?",
                "Theo sơ đồ tư duy ở Trang 98, ngành bưu chính viễn thông có những vai trò chủ yếu nào đối với phát triển kinh tế?",
                "Dựa vào Hình 34.6 và nội dung trang 96, hãy kể tên 4 sân bay quốc tế vận chuyển hành khách lớn nhất thế giới năm 2019?",
                "Theo Hình 29.2 (Trang 84), trong cơ cấu tiêu thụ năng lượng thế giới năm 2020, ba nguồn năng lượng chiếm tỉ trọng lớn nhất là gì?",
                "Kết hợp Bảng 19.1 (Trang 56) và Bảng 20 (Trang 61), quy mô dân số và tỉ lệ dân thành thị toàn thế giới thay đổi như thế nào?",
                "Chiến lược phát triển kinh tế biển Việt Nam đến năm 2030 theo Nghị quyết số 36-NQ/TW xác định những khâu đột phá nào?"
            ]
        else:
            sample_q_list = [
                "Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo nào và bởi ai?",
                "Vì sao không thể cộng trực tiếp điểm số của Vector Search và BM25 trong Hybrid Search?",
                "Sau khi qua bước Cross-Encoder trong Re-ranking, mô hình có thể giải quyết được mối quan hệ gì?",
                "Giới hạn số lượng tokens tối đa mà LLM có thể tiếp nhận và xử lý trong một lần prompt được gọi là gì?",
                "Hậu quả khi bước Phase 2: Retrieval truy xuất sai hoặc thiếu thông tin là gì?",
                "Đường dẫn mặc định persist_dir được thiết lập để lưu trữ database trong phần thực hành là gì?"
            ]
        chosen_sample = st.selectbox("Chọn câu truy vấn thử nghiệm:", options=sample_q_list)
    with col_q2:
        if is_bonus:
            section_filter = st.selectbox("Lọc Metadata:", options=["(Không lọc)"])
        else:
            section_filter = st.selectbox(
                "Lọc Section (Metadata Filter):",
                options=["(Không lọc)", "phan_tich_vai_tro", "gioi_thieu_langchain", "cac_thanh_phan_cot_loi", "vector_stores_va_retrievers", "thao_luan_on_tap"]
            )

    retrieval_query = st.text_input("Hoặc gõ câu truy vấn bất kỳ:", value=chosen_sample)
    search_now = st.button("🔎 Thực hiện Retrieval trên 4 Phương Pháp", type="primary")

    if search_now and retrieval_query.strip():
        if not retrievers:
            st.error("Kho dữ liệu Retrieval chưa được nạp.")
        else:
            filter_dict = None
            if section_filter != "(Không lọc)":
                filter_dict = {"section": section_filter}

            with st.spinner("Đang chạy đồng thời 4 thuật toán retrieval..."):
                t0 = time.perf_counter()
                res_dense = retrievers["dense"].search(retrieval_query, top_k=top_k, filters=filter_dict)
                t_dense = (time.perf_counter() - t0) * 1000

                t0 = time.perf_counter()
                res_bm25 = retrievers["bm25"].search(retrieval_query, top_k=top_k, filters=filter_dict)
                t_bm25 = (time.perf_counter() - t0) * 1000

                t0 = time.perf_counter()
                res_hybrid = retrievers["hybrid"].search(retrieval_query, top_k=top_k, filters=filter_dict)
                t_hybrid = (time.perf_counter() - t0) * 1000

                t0 = time.perf_counter()
                res_qt = retrievers["query_transform"].search(retrieval_query, top_k=top_k, filters=filter_dict)
                t_qt = (time.perf_counter() - t0) * 1000

            col_d, col_b, col_h, col_q = st.columns(4)

            def render_results(title, results, latency, badge_text):
                st.markdown(f"#### {title}")
                st.caption(f"⏱️ {latency:.2f}ms | {badge_text}")
                for idx, r in enumerate(results, 1):
                    score_str = f"Score: {r['score']:.4f}" if isinstance(r.get('score'), float) else ""
                    st.markdown(
                        f"""<div class="chunk-card">
                        <b>#{idx} [{r['id']}]</b> — Trang {r['page']} <br>
                        <small style="color: #6B7280;">{score_str}</small>
                        <p style="font-size:0.85rem; margin-top:6px;">{r['text'][:220]}...</p>
                        </div>""",
                        unsafe_allow_html=True
                    )

            with col_d:
                render_results("1. Dense (EmbeddingGemma)", res_dense, t_dense, "Qdrant Cosine")
            with col_b:
                render_results("2. BM25 (Lexical)", res_bm25, t_bm25, "BM25Okapi NFC")
            with col_h:
                render_results("3. Hybrid RRF (k=60)", res_hybrid, t_hybrid, "⭐ Tối Ưu Nhất")
            with col_q:
                render_results("4. Query Transform", res_qt, t_qt, "Keyword Expansion")


# =========================================================================
# TAB 3: DATA INGESTION EXPLORER
# =========================================================================
with tab_data:
    if is_bonus:
        st.markdown("### 📊 Khám Phá Tập Dữ Liệu SGK Địa lí 10 (Multimodal Ingestion)")
        st.markdown(
            "Tài liệu gốc: `assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf` (118 trang vật lý). "
            "Ingestion phân tách 32 chunks đa phương thức chất lượng cao: **11 Bảng số liệu**, **10 Sơ đồ/Bản đồ**, "
            "**6 Biểu đồ**, và **5 Khối văn bản chuyên đề**."
        )

        type_counts = {}
        chapter_counts = {}
        for c in chunks:
            m = c.get("metadata", {})
            ctype = m.get("content_type", "other")
            chap = m.get("chapter", "Khác")
            type_counts[ctype] = type_counts.get(ctype, 0) + 1
            chapter_counts[chap] = chapter_counts.get(chap, 0) + 1

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📌 Phân bố theo Định dạng Đa phương thức")
            df_type = pd.DataFrame(list(type_counts.items()), columns=["Loại thành phần", "Số lượng chunks"]).sort_values("Số lượng chunks", ascending=False)
            st.bar_chart(df_type.set_index("Loại thành phần"))

        with c2:
            st.markdown("##### 📚 Phân bố theo Chương SGK Địa lí 10")
            df_chap = pd.DataFrame(list(chapter_counts.items()), columns=["Chương", "Số lượng chunks"]).sort_values("Số lượng chunks", ascending=False)
            st.bar_chart(df_chap.set_index("Chương"))

    else:
        st.markdown("### 📊 Khám Phá Tập Dữ Liệu & Ingestion Chiến Lược B (Day 6)")
        st.markdown(
            "Kế thừa trực tiếp tập tài liệu chuyên sâu `AIO2025_Tutorial_RAG.pdf` của AI VIET NAM. "
            "Chiến lược B (Paragraph-based Semantic Chunking) phân tách 32 trang tài liệu thành 97 chunks tự nhiên, "
            "chuẩn hóa tiếng Việt NFC và bảo toàn metadata theo section."
        )
        sec_counts = {}
        page_counts = {}
        for c in chunks:
            sec = c.get("metadata", {}).get("section", "khac")
            sec_counts[sec] = sec_counts.get(sec, 0) + 1
            p = c.get("page", 0)
            page_counts[p] = page_counts.get(p, 0) + 1

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("##### 📌 Phân bố Chunk theo Chuyên mục (Section)")
            df_sec = pd.DataFrame(list(sec_counts.items()), columns=["Section", "Số lượng chunks"]).sort_values("Số lượng chunks", ascending=False)
            st.bar_chart(df_sec.set_index("Section"))

        with c2:
            st.markdown("##### 📄 Phân bố Chunk theo Trang Tài liệu")
            df_page = pd.DataFrame(list(page_counts.items()), columns=["Trang", "Số lượng chunks"]).sort_values("Trang")
            st.line_chart(df_page.set_index("Trang"))

    st.markdown("---")
    st.markdown("#### 🔎 Trình Xem Chi Tiết Từng Đoạn Dữ Liệu (Chunk Viewer)")

    selected_cid = st.selectbox(
        "Chọn Chunk ID để xem nội dung chi tiết:",
        options=[f"[{c['id']}] - Trang {c['page']} - {c.get('metadata', {}).get('lesson') or c.get('metadata', {}).get('section', '')}" for c in chunks]
    )

    if selected_cid:
        cid = selected_cid.split(" ")[0].strip("[]")
        target_chunk = next((c for c in chunks if c["id"] == cid), None)
        if target_chunk:
            meta = target_chunk.get("metadata", {})
            st.markdown(f"**Chunk ID:** `{target_chunk['id']}` | **Nguồn:** `{target_chunk['source']}` | **Trang:** `{target_chunk['page']}`")
            if is_bonus:
                st.markdown(f"**Loại:** `{meta.get('content_type')}` | **Chương:** `{meta.get('chapter')}` | **Bài:** `{meta.get('lesson')}`")
            else:
                st.markdown(f"**Section:** `{meta.get('section')}` | **Chiến lược:** `{meta.get('strategy')}`")
            st.text_area("Nội dung văn bản / bảng nguyên văn:", value=target_chunk["text"], height=160, disabled=True)


# =========================================================================
# TAB 4: AUDIT BENCHMARK EXPLORER
# =========================================================================
with tab_audit:
    st.markdown(f"### 📋 Nhật Ký Audit Toàn Diện {len(agent_cases)} Câu Benchmark")
    st.markdown(
        "Xem xét chi tiết từng câu hỏi trong bộ dữ liệu kiểm thử chuẩn, bao gồm: "
        "bằng chứng vàng (Gold evidence), chuỗi sự kiện tìm kiếm (Tool Events), câu trả lời thực tế, "
        "mức chấm điểm (0/1/2) và lý do đánh giá khách quan."
    )

    dev_traces = bench_results.get("agent_dev_traces", [])
    test_traces = bench_results.get("agent_test_traces", [])
    dev_reviews = bench_results.get("agent_dev_reviews", [])
    test_reviews = bench_results.get("agent_test_reviews", [])

    review_map = {r["query_id"]: r for r in (dev_reviews + test_reviews) if isinstance(r, dict) and "query_id" in r}

    filter_split = st.radio(
        "Lọc theo Tập dữ liệu:",
        options=[f"Tất cả ({len(agent_cases)} câu)", f"Tập Dev ({len([c for c in agent_cases if c['split']=='dev'])} câu)", f"Tập Test ({len([c for c in agent_cases if c['split']=='test'])} câu)"],
        horizontal=True
    )

    all_cases_display = []
    if "Tất cả" in filter_split or "Dev" in filter_split:
        for tr in dev_traces:
            qid = tr.get("query_id")
            rev = review_map.get(qid, {})
            all_cases_display.append({"split": "dev", "trace": tr, "review": rev})
    if "Tất cả" in filter_split or "Test" in filter_split:
        for tr in test_traces:
            qid = tr.get("query_id")
            rev = review_map.get(qid, {})
            all_cases_display.append({"split": "test", "trace": tr, "review": rev})

    for item in all_cases_display:
        tr = item["trace"]
        rev = item["review"]
        case_id = tr.get("query_id")
        case_info = case_map.get(case_id, {})
        q_text = case_info.get("question", f"Câu hỏi {case_id}")
        ans_status = tr.get("status")
        answer = tr.get("answer", "")
        citations = tr.get("citations", [])

        grade = rev.get("answer_grade")
        abstain_ok = rev.get("abstention_correct")
        cat = case_info.get("category", "")

        grade_text = f"Mức {grade}/2" if grade is not None else ("Abstention Đúng ✅" if abstain_ok else "Abstention Sai ❌")
        split_badge = item['split'].upper()

        with st.expander(f"🔹 [{split_badge}] [{cat.upper()}] {case_id}: {q_text[:75]}... — {grade_text}"):
            st.markdown(f"**Câu hỏi:** {q_text}")
            st.markdown(f"**Danh mục:** `{cat}` | **Trạng thái Agent:** `{ans_status}` | **Đánh giá:** `{grade_text}`")
            if case_info.get("expected_answer"):
                st.markdown(f"**Đáp án kỳ vọng:** *{case_info.get('expected_answer')}*")

            st.markdown(f"**Câu trả lời của Agent:**\n> {answer}")
            if citations:
                st.markdown(f"**Trích dẫn:** `{citations}`")

            evs = tr.get("events", [])
            if evs:
                st.markdown("**Các bước gọi tool:**")
                for e in evs:
                    if e.get("event") == "search":
                        st.caption(f"- `search('{e.get('query')}')` -> nạp {len(e.get('context_ids', []))} chunks: `{e.get('context_ids', [])}`")


# =========================================================================
# TAB 5: LEADERBOARD & FORMAL REPORT
# =========================================================================
with tab_report:
    st.markdown("### 📈 Bảng Điểm Tổng Hợp & Đúc Rút Kỹ Thuật")

    if is_bonus:
        st.markdown("#### 1. Bảng Hiệu Năng Retrieval trên SGK Địa lí 10 (118 Trang)")
        df_bonus_ret = pd.DataFrame([
            {"Phương pháp": "Dense (EmbeddingGemma-2)", "Tập": "Dev", "Hit@1": "14/15 (93.3%)", "Hit@3": "15/15 (100.0%)", "Context Hit": "14/15 (93.3%)", "Độ trễ": "55.4 ms"},
            {"Phương pháp": "BM25Okapi Lexical", "Tập": "Dev", "Hit@1": "13/15 (86.7%)", "Hit@3": "15/15 (100.0%)", "Context Hit": "13/15 (86.7%)", "Độ trễ": "0.28 ms"},
            {"Phương pháp": "⭐ Hybrid RRF (k=60)", "Tập": "Dev", "Hit@1": "14/15 (93.3%)", "Hit@3": "15/15 (100.0%)", "Context Hit": "14/15 (93.3%)", "Độ trễ": "55.8 ms"},
            {"Phương pháp": "Dense (EmbeddingGemma-2)", "Tập": "Test", "Hit@1": "21/24 (87.5%)", "Hit@3": "24/24 (100.0%)", "Context Hit": "21/24 (87.5%)", "Độ trễ": "53.2 ms"},
            {"Phương pháp": "BM25Okapi Lexical", "Tập": "Test", "Hit@1": "21/24 (87.5%)", "Hit@3": "24/24 (100.0%)", "Context Hit": "21/24 (87.5%)", "Độ trễ": "0.32 ms"},
            {"Phương pháp": "⭐ Hybrid RRF (k=60)", "Tập": "Test", "Hit@1": "21/24 (87.5%)", "Hit@3": "24/24 (100.0%)", "Context Hit": "21/24 (87.5%)", "Độ trễ": "53.6 ms"},
        ])
        st.table(df_bonus_ret)

        st.markdown("#### 2. Bảng Phân Rã Hiệu Năng Agent trên Toàn Bộ 6 Danh Mục (Tập Test 30 Câu)")
        df_bonus_breakdown = pd.DataFrame([
            {"Danh mục": "1. Bảng số liệu (Table)", "Yêu cầu": ">= 6 câu", "Số câu kiểm thử": "6 câu", "Kết quả đạt": "6 / 6 (100.0%)", "Điểm Grounded Answer": "1.83 / 2 (Mức 2: 5, Mức 1: 1)"},
            {"Danh mục": "2. Ảnh, Sơ đồ / Bản đồ", "Yêu cầu": ">= 5 câu", "Số câu kiểm thử": "5 câu", "Kết quả đạt": "5 / 5 (100.0%)", "Điểm Grounded Answer": "2.00 / 2 (Mức 2: 5/5)"},
            {"Danh mục": "3. Biểu đồ (Chart)", "Yêu cầu": ">= 5 câu", "Số câu kiểm thử": "5 câu", "Kết quả đạt": "5 / 5 (100.0%)", "Điểm Grounded Answer": "2.00 / 2 (Mức 2: 5/5)"},
            {"Danh mục": "4. Multi-hop (Nhiều trang)", "Yêu cầu": ">= 4 câu", "Số câu kiểm thử": "4 câu", "Kết quả đạt": "4 / 4 (100.0%)", "Điểm Grounded Answer": "2.00 / 2 (Mức 2: 4/4)"},
            {"Danh mục": "5. Văn bản (Text)", "Yêu cầu": ">= 4 câu", "Số câu kiểm thử": "4 câu", "Kết quả đạt": "3 / 4 (75.0%)", "Điểm Grounded Answer": "1.50 / 2 (Mức 2: 3, Mức 0: 1)"},
            {"Danh mục": "6. Thiếu bằng chứng (Abstention)", "Yêu cầu": ">= 6 câu", "Số câu kiểm thử": "6 câu", "Kết quả đạt": "6 / 6 (100.0%)", "Điểm Grounded Answer": "Abstention Đúng 100%"},
            {"Danh mục": "⭐ TỔNG CỘNG TEST", "Yêu cầu": ">= 30 câu (Độ chính xác >= 90%)", "Số câu kiểm thử": "30 câu", "Kết quả đạt": "29 / 30 (96.67%)", "Điểm Grounded Answer": "1.875 / 2.0 (ĐẠT +15 ĐIỂM THƯỞNG)"}
        ])
        st.table(df_bonus_breakdown)

    else:
        st.markdown("#### 1. Bảng So Sánh Các Phương Pháp Retrieval (AIO2025)")
        df_retrieval_table = pd.DataFrame([
            {"Cấu hình": "Baseline (TF-IDF)", "Đặc trưng": "Lexical word-match, budget=800", "Tập": "dev", "Hit@1": "6/15 (40.0%)", "Hit@3": "10/15 (66.7%)", "Context Hit": "6/15 (40.0%)", "Độ trễ": "0.26 ms"},
            {"Cấu hình": "Phương pháp 2 (Dense)", "Đặc trưng": "EmbeddingGemma-2 + Qdrant, budget=800", "Tập": "dev", "Hit@1": "7/15 (46.7%)", "Hit@3": "11/15 (73.3%)", "Context Hit": "7/15 (46.7%)", "Độ trễ": "64.09 ms"},
            {"Cấu hình": "Phương pháp 3 (BM25)", "Đặc trưng": "BM25Okapi NFC, budget=800", "Tập": "dev", "Hit@1": "6/15 (40.0%)", "Hit@3": "11/15 (73.3%)", "Context Hit": "6/15 (40.0%)", "Độ trễ": "0.30 ms"},
            {"Cấu hình": "Cải thiện 1 (Filter)", "Đặc trưng": "Dense + Metadata Section Filter", "Tập": "dev", "Hit@1": "7/15 (46.7%)", "Hit@3": "11/15 (73.3%)", "Context Hit": "7/15 (46.7%)", "Độ trễ": "50.54 ms"},
            {"Cấu hình": "Cải thiện 2 (Query Transform)", "Đặc trưng": "Domain Keyword Expansion + Hybrid", "Tập": "dev", "Hit@1": "7/15 (46.7%)", "Hit@3": "12/15 (80.0%)", "Context Hit": "8/15 (53.3%)", "Độ trễ": "51.14 ms"},
            {"Cấu hình": "⭐ Phương pháp 4 (Hybrid RRF)", "Đặc trưng": "Dense + BM25 qua RRF (k=60), budget=800", "Tập": "dev", "Hit@1": "8/15 (53.3%)", "Hit@3": "13/15 (86.7%)", "Context Hit": "8/15 (53.3%)", "Độ trễ": "56.35 ms"},
            {"Cấu hình": "Baseline Đối Chứng (Dense)", "Đặc trưng": "Dense Retrieval thuần Day 6", "Tập": "test", "Hit@1": "3/5 (60.0%)", "Hit@3": "3/5 (60.0%)", "Context Hit": "2/5 (40.0%)", "Độ trễ": "50.93 ms"},
            {"Cấu hình": "⭐ Cấu hình Chọn (Hybrid RRF)", "Đặc trưng": "Đánh giá độc lập trên tập Test", "Tập": "test", "Hit@1": "2/5 (40.0%)", "Hit@3": "4/5 (80.0%)", "Context Hit": "1/5 (20.0%)", "Độ trễ": "51.63 ms"}
        ])
        st.table(df_retrieval_table)

        st.markdown("#### 2. Bảng Hiệu Năng Agentic RAG Controller")
        df_agent_table = pd.DataFrame([
            {"Cấu hình / Split": "Agent Initial (Hybrid) / Dev", "Tool Use %": "15/15 (100%)", "Số lượt gọi TB": "1.87", "Điểm Grounded Answer": "1.08 / 2", "Citation Hợp lệ": "100.0%", "Abstention Đúng": "2/2 (100.0%)", "Từ chối nhầm": "46.2%"},
            {"Cấu hình / Split": "⭐ Agent Cải tiến (Hybrid) / Dev", "Tool Use %": "16/16 (100%)", "Số lượt gọi TB": "1.94", "Điểm Grounded Answer": "1.33 / 2", "Citation Hợp lệ": "100.0%", "Abstention Đúng": "1/1 (100.0%)", "Từ chối nhầm": "26.7%"},
            {"Cấu hình / Split": "Agent Baseline (Dense) / Test", "Tool Use %": "6/6 (100%)", "Số lượt gọi TB": "1.83", "Điểm Grounded Answer": "1.00 / 2", "Citation Hợp lệ": "100.0%", "Abstention Đúng": "2/2 (100.0%)", "Từ chối nhầm": "50.0%"},
            {"Cấu hình / Split": "⭐ Agent Chọn (Hybrid RRF) / Test", "Tool Use %": "7/7 (100%)", "Số lượt gọi TB": "1.86", "Điểm Grounded Answer": "1.20 / 2", "Citation Hợp lệ": "100.0%", "Abstention Đúng": "2/2 (100.0%)", "Từ chối nhầm": "40.0%"}
        ])
        st.table(df_agent_table)

    st.markdown("---")
    st.markdown("📄 Xem chi tiết báo cáo nghiên cứu hoàn chỉnh: [`report/individual/2A202603976_HoangNgocHieu.md`](report/individual/2A202603976_HoangNgocHieu.md)")

st.markdown("---")
st.caption("Hoàng Ngọc Hiệu — MSSV: 2A202603976 — AI VIET NAM AI20K Lab 07")
