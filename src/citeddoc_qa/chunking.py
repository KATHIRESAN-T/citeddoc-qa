from __future__ import annotations

from dataclasses import dataclass

from citeddoc_qa.documents import Document


@dataclass(frozen=True)
class Chunk:
    id: str
    source: str
    chunk_number: int
    text: str


def chunk_documents(
    documents: list[Document],
    *,
    chunk_size_words: int = 180,
    overlap_words: int = 40,
) -> list[Chunk]:
    if overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be smaller than chunk_size_words")

    chunks: list[Chunk] = []
    for document in documents:
        words = document.text.split()
        start = 0
        chunk_number = 1
        step = chunk_size_words - overlap_words

        while start < len(words):
            end = min(start + chunk_size_words, len(words))
            text = " ".join(words[start:end]).strip()
            if text:
                chunks.append(
                    Chunk(
                        id=f"{document.source}#{chunk_number}",
                        source=document.source,
                        chunk_number=chunk_number,
                        text=text,
                    )
                )
            if end == len(words):
                break
            start += step
            chunk_number += 1

    return chunks

