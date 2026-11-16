"""Day 6 EmbeddingGemma-2 Adapter for Day 7 Dense Retrieval."""
import logging
import os
from typing import Protocol

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import torch
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class Day6Embedder:
    """Embedder using Google EmbeddingGemma-2 (768 dimensions), compatible with Day 6 store."""

    def __init__(self, model_name: str = "google/embeddinggemma-2", device: str | None = None) -> None:
        self.model_name = model_name
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        logger.info(f"Loading embedding model '{self.model_name}' on {self.device}...")
        self.model = SentenceTransformer(self.model_name, device=self.device)
        self.dimensions = int(self.model.get_embedding_dimension())
        logger.info(f"Loaded {self.model_name} (dim={self.dimensions}) on {self.device}")

    def embed_query(self, question: str) -> list[float]:
        """Embed user query with Google EmbeddingGemma QA query instruction format."""
        formatted_query = f"task: question answering | query: {question}"
        embedding = self.model.encode(
            [formatted_query],
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True
        )[0]
        return embedding.tolist()

    def embed_documents(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        """Embed document chunks using Google EmbeddingGemma document format."""
        if not texts:
            return []
        formatted_texts = [f"title: none | text: {t}" for t in texts]
        embeddings = self.model.encode(
            formatted_texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        return embeddings.tolist()
