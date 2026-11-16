"""Retrieval methods for Day 7: Dense, BM25 Lexical, and Hybrid RRF."""
import logging
import os
from typing import Any, Protocol

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from .embeddings import Day6Embedder
from .bm25 import BM25Index

logger = logging.getLogger(__name__)


class BaseRetriever(Protocol):
    def search(self, query: str, top_k: int = 3, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        ...


class DenseRetriever:
    """Dense retrieval querying Day 6 Qdrant collection with EmbeddingGemma-2."""

    def __init__(self, qdrant_path: str = "data/qdrant_db", collection_name: str = "chunks_strategy_b", embedder: Day6Embedder | None = None):
        self.qdrant_path = qdrant_path
        self.collection_name = collection_name
        self.embedder = embedder or Day6Embedder()
        self.client = QdrantClient(path=self.qdrant_path)

    def search(self, query: str, top_k: int = 3, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        query_vector = self.embedder.embed_query(query)

        query_filter = None
        if filters and "section" in filters:
            section_val = filters["section"]
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="section",
                        match=MatchValue(value=section_val)
                    )
                ]
            )

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True
        )

        results = []
        for rank, hit in enumerate(response.points, start=1):
            pl = hit.payload or {}
            results.append({
                "id": pl.get("chunk_id"),
                "source_id": pl.get("source_id") or pl.get("document_id"),
                "source": pl.get("source"),
                "page": int(pl.get("page", 0)),
                "text": pl.get("text", ""),
                "metadata": pl.get("metadata", {}),
                "score": float(hit.score) if hit.score is not None else 0.0,
                "rank": rank,
                "retriever": "dense"
            })
        return results

    def close(self):
        self.client.close()


class BM25Retriever:
    """Lexical retrieval using BM25Okapi."""

    def __init__(self, chunks: list[dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.index = BM25Index(chunks, k1=k1, b=b)

    def search(self, query: str, top_k: int = 3, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        section_val = filters.get("section") if filters else None
        return self.index.search(query, top_k=top_k, section_filter=section_val)


class HybridRetriever:
    """Hybrid retrieval combining Dense and BM25 using Reciprocal Rank Fusion (RRF)."""

    def __init__(self, dense_retriever: DenseRetriever, bm25_retriever: BM25Retriever, rrf_k: int = 60):
        self.dense = dense_retriever
        self.bm25 = bm25_retriever
        self.rrf_k = rrf_k

    def search(self, query: str, top_k: int = 3, filters: dict[str, Any] | None = None, candidate_k: int = 10) -> list[dict[str, Any]]:
        # Retrieve candidates from both systems
        dense_results = self.dense.search(query, top_k=candidate_k, filters=filters)
        bm25_results = self.bm25.search(query, top_k=candidate_k, filters=filters)

        # Map by chunk id
        scores: dict[str, float] = {}
        chunk_map: dict[str, dict[str, Any]] = {}
        ranks_dense: dict[str, int] = {}
        ranks_bm25: dict[str, int] = {}

        for rank, item in enumerate(dense_results, start=1):
            cid = item["id"]
            chunk_map[cid] = item
            ranks_dense[cid] = rank
            scores[cid] = scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        for rank, item in enumerate(bm25_results, start=1):
            cid = item["id"]
            if cid not in chunk_map:
                chunk_map[cid] = item
            ranks_bm25[cid] = rank
            scores[cid] = scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        # Sort by RRF score descending
        sorted_cids = sorted(scores.keys(), key=lambda cid: (-scores[cid], cid))

        results = []
        for rank, cid in enumerate(sorted_cids[:top_k], start=1):
            item = dict(chunk_map[cid])
            item["score"] = scores[cid]
            item["rank"] = rank
            item["retriever"] = "hybrid_rrf"
            item["dense_rank"] = ranks_dense.get(cid)
            item["bm25_rank"] = ranks_bm25.get(cid)
            results.append(item)

        return results


class QueryTransformHybridRetriever:
    """Hybrid retrieval with query transformation (domain keyword expansion + multi-query)."""

    # Domain vocabulary map for Vietnamese RAG queries
    DOMAIN_SYNONYMS = {
        "context window": ["cửa sổ ngữ cảnh", "giới hạn token", "độ dài context"],
        "grounding": ["neo dữ liệu", "tính xác thực", "chống hallucination"],
        "hallucination": ["ảo giác", "bịa đặt", "thông tin sai lệch"],
        "rrf": ["reciprocal rank fusion", "hợp nhất xếp hạng", "hybrid search"],
        "generator": ["mô hình sinh", "sinh văn bản", "BART", "LLM"],
        "retriever": ["truy xuất", "tìm kiếm vector", "dense retrieval"],
        "phase 1": ["ingestion", "chunking", "tiền xử lý", "nạp dữ liệu"],
        "phase 2": ["retrieval", "tìm kiếm", "rerank", "hybrid"],
        "phase 3": ["generation", "sinh câu trả lời", "chuỗi suy nghĩ", "CoT"]
    }

    def __init__(self, hybrid_retriever: HybridRetriever):
        self.hybrid = hybrid_retriever

    def transform_query(self, query: str) -> str:
        """Expand query with relevant technical keywords if detected."""
        q_lower = query.lower()
        expanded_terms = []
        for key, synonyms in self.DOMAIN_SYNONYMS.items():
            if key in q_lower or any(s in q_lower for s in synonyms):
                expanded_terms.append(key)
        if expanded_terms:
            return f"{query} ({', '.join(expanded_terms)})"
        return query

    def search(self, query: str, top_k: int = 3, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        expanded_query = self.transform_query(query)
        results = self.hybrid.search(expanded_query, top_k=top_k, filters=filters)
        for r in results:
            r["retriever"] = "query_transform_hybrid"
            r["transformed_query"] = expanded_query
        return results
