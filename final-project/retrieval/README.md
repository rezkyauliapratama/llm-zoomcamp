# Retrieval Layer

Hybrid search pipeline combining dense (vector) and sparse (keyword) retrieval with RRF fusion and cross-encoder reranking.

## Architecture

```
User Query
    ↓
Query Rewriter (LLM) → expands abbreviations, adds regulatory context
    ↓                      ↓
PGVector Search      PostgreSQL FTS (tsvector)
(dense/vector)       (sparse/keyword)
    ↓                      ↓
         RRF Fusion (k=60)
              ↓
    Cross-Encoder Reranker
    (top-10 → top-5)
              ↓
    Retrieved Chunks with scores
```

## Components

- `hybrid_search.py` — RRF fusion of vector + keyword results
- `reranker.py` — Cross-encoder reranking (`cross-encoder/ms-marco-MiniLM-L-6-v2`)
- `query_rewriter.py` — LLM-based query expansion for regulatory queries

## Search Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Vector Top K | 10 | PGVector cosine similarity |
| FTS Top K | 10 | PostgreSQL tsvector BM25-like |
| RRF k constant | 60 | Standard smoothing constant |
| Reranker Top K | 5 | Final chunks passed to LLM |
| Embedding model | `intfloat/multilingual-e5-base` | 768-dim, bilingual |
| Vector index | HNSW (m=16, ef=64) | Fast ANN search |
