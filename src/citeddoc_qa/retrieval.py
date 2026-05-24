from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from citeddoc_qa.chunking import Chunk


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float


class TfidfRetriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        if not chunks:
            raise ValueError("At least one chunk is required")

        self.chunks = chunks
        self.term_counts = [Counter(_tokenize(chunk.text)) for chunk in chunks]
        self.doc_freqs = _document_frequencies(self.term_counts)
        self.idf = {
            term: math.log((1 + len(chunks)) / (1 + freq)) + 1
            for term, freq in self.doc_freqs.items()
        }
        self.vectors = [self._vectorize_counts(counts) for counts in self.term_counts]

    def search(self, query: str, *, k: int = 4) -> list[SearchResult]:
        query_counts = Counter(_tokenize(query))
        query_vector = self._vectorize_counts(query_counts)
        scored = [
            SearchResult(chunk=chunk, score=_cosine(query_vector, vector))
            for chunk, vector in zip(self.chunks, self.vectors)
        ]
        return [result for result in sorted(scored, key=lambda item: item.score, reverse=True)[:k] if result.score > 0]

    def _vectorize_counts(self, counts: Counter[str]) -> dict[str, float]:
        total = sum(counts.values()) or 1
        return {
            term: (count / total) * self.idf.get(term, 1.0)
            for term, count in counts.items()
        }


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def _document_frequencies(term_counts: list[Counter[str]]) -> Counter[str]:
    freqs: Counter[str] = Counter()
    for counts in term_counts:
        freqs.update(counts.keys())
    return freqs


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0

    numerator = sum(value * right.get(term, 0.0) for term, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)

