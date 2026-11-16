"""BM25 (BM25Okapi) implementation for Day 7 Lexical Retrieval."""
import math
import re
import unicodedata
from collections import Counter
from typing import Any


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase words with NFC normalization."""
    normalized = unicodedata.normalize('NFC', text or "")
    return re.findall(r'\w+', normalized.casefold())


class BM25Index:
    """BM25Okapi implementation for lexical search on document chunks."""

    def __init__(self, chunks: list[dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.corpus_size = len(chunks)

        self.doc_tokens = [tokenize(c["text"]) for c in chunks]
        self.doc_lens = [len(t) for t in self.doc_tokens]
        self.avgdl = sum(self.doc_lens) / self.corpus_size if self.corpus_size > 0 else 1.0

        # Term frequencies per document
        self.doc_freqs = [Counter(tokens) for tokens in self.doc_tokens]

        # Document frequencies across corpus
        df = Counter()
        for freqs in self.doc_freqs:
            for term in freqs:
                df[term] += 1

        # Calculate IDF with Robertson-Spärck Jones formula (with floor at 0)
        self.idf = {}
        for term, freq in df.items():
            idf_val = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)
            self.idf[term] = max(idf_val, 1e-4)

    def search(self, query: str, top_k: int = 3, section_filter: str | None = None) -> list[dict[str, Any]]:
        """Score and rank chunks for a given query."""
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        scores = []
        for i, (chunk, freqs, doc_len) in enumerate(zip(self.chunks, self.doc_freqs, self.doc_lens)):
            # Apply metadata filter if requested
            if section_filter:
                sec = chunk.get("metadata", {}).get("section") or chunk.get("section")
                if sec != section_filter:
                    continue

            score = 0.0
            for token in query_tokens:
                if token not in self.idf:
                    continue
                tf = freqs.get(token, 0)
                if tf == 0:
                    continue
                idf = self.idf[token]
                # BM25 formula
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avgdl))
                score += idf * (numerator / denominator)

            if score > 0:
                scores.append((score, chunk))

        # Sort by score descending, then chunk id
        scores.sort(key=lambda x: (-x[0], x[1]["id"]))

        results = []
        for rank, (score, chunk) in enumerate(scores[:top_k], start=1):
            results.append({
                **chunk,
                "score": score,
                "rank": rank,
                "retriever": "bm25"
            })
        return results
