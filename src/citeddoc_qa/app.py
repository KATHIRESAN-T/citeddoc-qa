from __future__ import annotations

import argparse
from pathlib import Path

from citeddoc_qa.chunking import chunk_documents
from citeddoc_qa.documents import load_documents
from citeddoc_qa.llm import answer_with_llm
from citeddoc_qa.retrieval import TfidfRetriever


DEFAULT_DOCS = Path(__file__).resolve().parents[2] / "data" / "sample_docs"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask cited questions over local documents.")
    parser.add_argument("question", help="Natural-language question to answer")
    parser.add_argument("--docs", default=str(DEFAULT_DOCS), help="Folder containing .md, .txt, or .pdf files")
    parser.add_argument("--top-k", type=int, default=4, help="Number of chunks to pass to the answer step")
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv
    except ImportError:
        pass
    else:
        load_dotenv()
    documents = load_documents(Path(args.docs))
    chunks = chunk_documents(documents)
    retriever = TfidfRetriever(chunks)
    results = retriever.search(args.question, k=args.top_k)
    answer = answer_with_llm(args.question, results)

    print("Answer:")
    print(answer)
    print()
    print("Citations:")
    if not results:
        print("No citations available.")
        return

    for index, result in enumerate(results, start=1):
        print(f"[{index}] {result.chunk.source}, chunk {result.chunk.chunk_number} (score: {result.score:.3f})")


if __name__ == "__main__":
    main()
