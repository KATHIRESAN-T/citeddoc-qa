import unittest

from citeddoc_qa.chunking import chunk_documents
from citeddoc_qa.documents import Document
from citeddoc_qa.retrieval import TfidfRetriever


class RetrievalTests(unittest.TestCase):
    def test_retriever_finds_refund_policy(self) -> None:
        documents = [
            Document(source="refund.md", text="Refund requests are allowed within 14 calendar days."),
            Document(source="remote.md", text="Remote work requires manager approval."),
        ]
        chunks = chunk_documents(documents, chunk_size_words=20, overlap_words=5)
        retriever = TfidfRetriever(chunks)

        results = retriever.search("When can a customer get a refund?", k=1)

        self.assertTrue(results)
        self.assertEqual(results[0].chunk.source, "refund.md")


if __name__ == "__main__":
    unittest.main()
