# Module 04 — Evaluation

Homework submission for [LLM Zoomcamp 2026 Cohort](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026/04-evaluation).

---

## Overview

This homework evaluates search quality using ground truth data. We build text, vector, and hybrid search over 72 course lesson pages, then measure performance with Hit Rate and MRR.

Concepts covered:
- Generating ground truth questions with an LLM (structured output)
- Building text (keyword), vector, and hybrid search
- Evaluating retrieval with Hit Rate and MRR
- Tuning RRF hybrid search parameters

---

## Setup

### Prerequisites

- Python 3.12+
- uv package manager
- OpenAI API key (or any OpenAI-compatible provider)

### Installation

```bash
cp .env.template .env
# Edit .env with your API key

uv sync
```

### Download helper files

```bash
PREFIX=https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main
wget ${PREFIX}/cohorts/2026/04-evaluation/ground-truth.csv
```

---

## Running

```bash
uv run python homework.py
```

This will run all 6 homework questions and print the answers. Q1 requires an LLM call with your API key. Results are approximate and may vary between runs.

---

## Homework Answers

### Q1 — Average input tokens for generating questions

**Answer: ~1400**

Generate 5 questions per page for the first 3 lesson pages. The average input tokens across 3 calls is around 1,400. Options: 140, 1400, 14000, 140000.

### Q2 — First result with text search

**Answer: 01-agentic-rag/lessons/03-rag.md**

Text (keyword) search for the first ground truth question (about RAG) returns the RAG lesson page because it contains the keywords "retrieval-augmented generation".

### Q3 — First result with vector search

**Answer: 01-agentic-rag/lessons/01-intro.md**

Vector search returns the correct source page (01-intro.md) because semantic similarity matches the question's meaning to the intro content, not just keyword overlap.

> This illustrates the key difference: text search matches words, vector search matches meaning.

### Q4 — Text search Hit Rate

**Answer: ~0.66 (varies by run)**

Keyword search correctly retrieves the right page for about 66% of the 360 questions.

### Q5 — Vector search MRR

**Answer: ~0.55 (varies by run)**

Vector search has a lower MRR than text search on this dataset because course terms are often technical and precise (e.g., "pgvector", "sqlitesearch", "RRF"), which keyword search handles better.

### Q6 — Best k for hybrid search RRF

**Answer: 100 (varies by run)**

k=100 balances rank contributions from both search methods. Too small (k=1) makes only top results matter; too large (k=200) dilutes the ranking signal.

---

## Submission

Submit your answers at:
[https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4](https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4)

Make sure to include a link to your GitHub repository.
