# CitedDoc QA

A small Retrieval-Augmented Generation (RAG) project that answers questions over a local
document folder and returns citations for the chunks used as evidence.

This project was built for an AI/ML screening assignment to demonstrate practical LLM
integration, retrieval design, prompt grounding, and failure handling. It is intentionally
small enough to run locally, but the structure mirrors a production document Q&A system:
ingestion, chunking, retrieval, prompt construction, LLM generation, and citation display.

## Features

- Loads `.md`, `.txt`, and `.pdf` files from a local folder
- Splits documents into overlapping chunks with source metadata
- Retrieves relevant chunks using a lightweight TF-IDF index
- Calls the OpenAI Responses API to generate grounded answers
- Falls back to an extractive answer when `OPENAI_API_KEY` is not set
- Shows citations with file names and chunk numbers
- Includes sample company-policy documents for a quick demo

## Architecture

```text
documents/ -> loader -> chunker -> TF-IDF index -> retriever -> prompt builder -> LLM -> answer + citations
```

The important design choice is that the LLM is not asked to answer from memory. The
retriever first selects the most relevant chunks, and the prompt instructs the model to
answer only from the supplied context. If the evidence is incomplete, the app says so.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your OpenAI key:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5
```

`OPENAI_MODEL` is configurable because model availability changes over time.

## Run The Demo

Without an API key, the app still demonstrates retrieval and citations:

```powershell
python -m citeddoc_qa.app "What is the refund policy?"
```

With an API key, the same command uses the OpenAI Responses API:

```powershell
python -m citeddoc_qa.app "Can employees work remotely and what approval is needed?"
```

Use your own folder:

```powershell
python -m citeddoc_qa.app "What are the support SLAs?" --docs path\to\docs
```

If you run from the repository root without installing the package, set `PYTHONPATH` first:

```powershell
$env:PYTHONPATH="src"
python -m citeddoc_qa.app "What is the refund policy?"
```

## Run Tests

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

## Example Output

```text
Answer:
Customers can request a refund within 14 calendar days of purchase if onboarding has not
started and fewer than 20 percent of included credits have been used.

Citations:
[1] refund_policy.md, chunk 1
```

## Engineering Challenge

The hardest part was reducing hallucination risk. A naive LLM prompt can produce confident
answers even when the retrieved context only partially answers the question. This project
mitigates that by:

- separating retrieval from generation
- passing compact citations into the prompt
- requiring the model to state when evidence is incomplete
- providing an extractive fallback when no API key is configured

## Limitations

- The local retriever uses TF-IDF instead of semantic embeddings to keep the demo easy to
  run. In production, this should be replaced or combined with embeddings and hybrid search.
- PDF extraction depends on text being selectable; scanned PDFs need OCR.
- The command-line interface is intentionally minimal.

## Suggested Demo Video Script

1. Show the repository structure.
2. Open `data/sample_docs/refund_policy.md` and `remote_work.md`.
3. Run `python -m citeddoc_qa.app "What is the refund policy?"`.
4. Point out the cited source file and chunk.
5. Ask a partial question, such as `What is the hardware replacement timeline?`, and show
   that the system avoids inventing details when the documents do not contain enough proof.
