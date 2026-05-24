from __future__ import annotations

import os
from textwrap import dedent

from citeddoc_qa.retrieval import SearchResult


SYSTEM_INSTRUCTIONS = """You are a careful document Q&A assistant.
Answer only from the provided evidence.
If the evidence is incomplete, say what is known and what is missing.
Cite sources using bracket numbers like [1] and [2].
Do not invent policies, dates, prices, or names."""


def answer_with_llm(question: str, results: list[SearchResult]) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return answer_without_llm(question, results)

    from openai import OpenAI

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5")
    prompt = _build_prompt(question, results)
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
    )
    return response.output_text.strip()


def answer_without_llm(question: str, results: list[SearchResult]) -> str:
    if not results:
        return (
            "No relevant evidence was found in the indexed documents. "
            "I cannot answer this from the provided corpus."
        )

    best = results[0].chunk
    return (
        "OpenAI API key not configured, so showing the strongest retrieved evidence "
        f"instead of a generated answer.\n\n{best.text}\n\n[1]"
    )


def _build_prompt(question: str, results: list[SearchResult]) -> str:
    evidence = "\n\n".join(
        f"[{index}] Source: {result.chunk.source}, chunk {result.chunk.chunk_number}\n"
        f"{result.chunk.text}"
        for index, result in enumerate(results, start=1)
    )
    return dedent(
        f"""
        Question:
        {question}

        Evidence:
        {evidence if evidence else "No relevant evidence found."}

        Write a concise answer with citations. If the evidence is not enough, say so.
        """
    ).strip()
