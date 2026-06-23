# Module 04 - Evaluation: Homework

> **Source:** [DataTalksClub/llm-zoomcamp/cohorts/2026/04-evaluation/](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026)

## Overview

Modul ini membahas cara mengevaluasi RAG pipeline secara sistematis.

**Key Topics:**
- Ground truth dataset generation (synthetic Q&A)
- Retrieval metrics: Hit Rate@k, MRR (Mean Reciprocal Rank)
- LLM-as-a-Judge evaluation
- Comparing multiple retrieval approaches

## Files Structure

```
module-04-evaluation/
├── README.md               ← this file
├── notebook.ipynb          ← main homework notebook
├── generate_ground_truth.py← script to generate synthetic QA
├── evaluate_retrieval.py   ← Hit Rate + MRR evaluation
├── evaluate_rag.py         ← LLM-as-a-Judge evaluation
├── data/
│   └── ground_truth.csv    ← generated Q&A pairs (gitignored if large)
├── requirements.txt        ← pinned dependencies
└── answers.md              ← submitted answers
```

## Setup

```bash
cd homework/module-04-evaluation
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```
