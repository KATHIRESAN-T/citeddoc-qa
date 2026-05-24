from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


@dataclass(frozen=True)
class Document:
    source: str
    text: str


def load_documents(directory: Path) -> list[Document]:
    if not directory.exists():
        raise FileNotFoundError(f"Document folder does not exist: {directory}")

    documents: list[Document] = []
    for path in sorted(directory.rglob("*")):
        if path.is_dir() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = _read_file(path)
        if text.strip():
            documents.append(Document(source=path.name, text=text.strip()))

    if not documents:
        raise ValueError(f"No supported documents found in {directory}")

    return documents


def _read_file(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    return path.read_text(encoding="utf-8")

