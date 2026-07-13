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

**Answer: 0.76**

Keyword search correctly retrieves the right page for about 76% of the 360 questions. Options: 0.55, 0.66, 0.76, 0.88.

### Q5 — Vector search MRR

**Answer: 0.64 (closest to 0.65)**

Vector search MRR is 0.64 on this run. Options: 0.35, 0.45, 0.55, 0.65.

> Note: Vector search has a higher Hit Rate (0.81) but lower MRR compared to text search, meaning it finds the right page more often but ranks it lower on average.

### Q6 — Best k for hybrid search RRF

**Answer: k=1**

| k | Hit Rate | MRR |
|---|----------|----:|
| 1 | 0.858 | 0.672 |
| 50 | 0.847 | 0.672 |
| 100 | 0.847 | 0.672 |
| 200 | 0.847 | 0.672 |

k=1 gives the best MRR (tied with others) and the highest Hit Rate. Per the homework: if multiple k values have the same MRR, pick the smallest k.

---
