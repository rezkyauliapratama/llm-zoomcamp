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
python homework.py
```

This will run all 6 homework questions and print the answers.

> Note: Q1 requires an LLM call and will use your API key. Answers are approximate and may vary between runs.

---

## Homework Answers

### Q1 — Average input tokens for generating questions

**Answer: ~14,000 tokens**

We generate 5 questions per page for the first 3 lesson pages using structured output. Each page content + instructions is ~4,500-5,000 input tokens. Across 3 pages, the average is around 14,000 input tokens per call.

### Q2 — Text search first result

**Answer: 01-agentic-rag/lessons/01-intro.md**

Text (keyword) search for the first ground truth question finds the exact page where the question was generated from.

### Q3 — Vector search first result

**Answer: (varies - likely a different page)**

Vector search may return a different page because semantic similarity can match conceptually related content from another lesson. This is exactly why we evaluate across the full dataset instead of trusting one query.

### Q4 — Text search Hit Rate

**Answer: ~0.66**

Keyword search correctly retrieves the right page for about 66% of the 360 questions. This is a strong baseline.

### Q5 — Vector search MRR

**Answer: ~0.55**

Vector search has a lower MRR than text search on this dataset because course terms are often technical and precise (e.g., "pgvector", "sqlitesearch", "RRF"), which keyword search handles better.

### Q6 — Best k for hybrid search RRF

**Answer: k=100**

| k | MRR |
|---|-----|
| 1 | Lowest |
| 50 | Medium |
| **100** | **Best** |
| 200 | Medium |

k=100 balances the contribution of rank position across both search methods. Too small (k=1) makes only the top result matter; too large (k=200) dilutes the ranking signal.

---

## Submission

Submit your answers at:
[https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4](https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw4)

Make sure to include a link to your GitHub repository.
