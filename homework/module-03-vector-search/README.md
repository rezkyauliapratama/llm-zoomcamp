# Module 03 - Vector Search & Retrieval: Homework

> **Source:** [DataTalksClub/llm-zoomcamp/cohorts/2026/03-vector-search/](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026)

## Overview

Modul ini mencakup vector embeddings, similarity search, dan hybrid search.

**Key Topics:**
- Text embeddings (sentence-transformers, OpenAI embeddings)
- PGVector setup dan HNSW index
- Elasticsearch dense vector search
- BM25 keyword search
- Hybrid search: RRF (Reciprocal Rank Fusion)

## Files Structure

```
module-03-vector-search/
├── README.md               ← this file
├── notebook.ipynb          ← main homework notebook
├── requirements.txt        ← pinned dependencies
├── docker-compose.yaml     ← Elasticsearch / PGVector setup
└── answers.md              ← submitted answers
```

## Setup

```bash
cd homework/module-03-vector-search
docker-compose up -d

uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```
