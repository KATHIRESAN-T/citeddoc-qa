# Assignment Section 1: LLM Project

I had not completed a production-level LLM application before receiving this screening
assignment, so I did not want to fabricate prior experience. To demonstrate my current
ability, I built a small LLM-backed document Q&A project called **CitedDoc QA**.

## Problem Solved

Many internal documents contain useful policy information, but users often do not know
which file contains the answer. CitedDoc QA lets a user ask a natural-language question
over a local document folder and returns an answer grounded in retrieved document chunks,
with citations showing which files were used.

Example questions:

- What is the refund policy?
- Can employees work remotely and what approval is needed?
- What are the support SLAs for Priority 1 incidents?

## High-Level Architecture

The project has five main components:

1. **Document loader**
   Loads `.md`, `.txt`, and `.pdf` files from a local folder. PDF support is handled with
   `pypdf`.

2. **Chunker**
   Splits documents into overlapping word chunks. The overlap reduces the chance that an
   answer is separated across two chunks.

3. **Retriever**
   Builds a lightweight TF-IDF index and returns the most relevant chunks for a user
   question. This keeps the demo simple and runnable without external infrastructure.

4. **Prompt builder**
   Creates a grounded prompt containing only the retrieved evidence. The model is instructed
   to answer only from the evidence and to say when information is missing.

5. **LLM answer generator**
   Uses the OpenAI Responses API when `OPENAI_API_KEY` is configured. If no key is present,
   the app falls back to showing the best retrieved evidence so the retrieval behavior can
   still be demonstrated.

## Engineering Challenge

The main challenge was reducing hallucination risk. In a basic LLM wrapper, the model may
answer from general knowledge even when the documents do not support the answer. I addressed
this by separating retrieval from generation, passing citations into the prompt, and
instructing the model to say when the evidence is incomplete.

Another practical challenge was making the project demo-friendly. A reviewer should be able
to run the project even without an API key, so I added an extractive fallback mode that
prints the strongest retrieved evidence with citations.

## Repository And Demo

Repository link: https://github.com/KATHIRESAN-T/citeddoc-qa

Demo video link: TODO after recording a short screen capture
