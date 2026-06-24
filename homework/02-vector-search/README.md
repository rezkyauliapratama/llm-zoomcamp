# Homework 02 — Vector Search

## Setup

```bash
# Install dependencies (reads pyproject.toml)
uv sync

# Download the ONNX model (Xenova/all-MiniLM-L6-v2)
uv run python download.py

# Run the solution
uv run python homework.py
```

> Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/#installation).

---

## Questions & Answers

### Q1. Embedding a query

Embed the query "How does approximate nearest neighbor search work?" using the ONNX Embedder.

**Result:** `v[0] = -0.0206` → Closest option: **-0.02**

### Q2. Cosine similarity

Load the page `02-vector-search/lessons/07-sqlitesearch-vector.md`, embed its content, and compute cosine similarity with the Q1 query vector.

**Result:** `cosine_sim = 0.3611` → Closest option: **0.37**

### Q3. Chunking and search by hand

Chunk all 72 lesson pages (size=2000, step=1000), embed all chunks, score against the Q1 query.

**Result:** Top chunk is `02-vector-search/lessons/07-sqlitesearch-vector.md` (start=1000, score=0.6489)

### Q4. Vector search with minsearch

Use `VectorSearch` from minsearch to search "What metric do we use to evaluate a search engine?"

**Result:** First result is `04-evaluation/lessons/05-search-metrics.md`

### Q5. Text search vs vector search

Compare keyword search vs vector search for "How do I store vectors in PostgreSQL?"

**Result:** File in vector results but NOT in text results: `02-vector-search/lessons/08-pgvector.md`

### Q6. Hybrid search (RRF)

Combine vector + text search results using Reciprocal Rank Fusion (k=60) for "How do I give the model access to tools?"

**Result:** First result after RRF: `01-agentic-rag/lessons/13-function-calling.md`

---

## Submit

Submit answers at: https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw2

> It's possible your answers won't match exactly. If so, select the closest one.
