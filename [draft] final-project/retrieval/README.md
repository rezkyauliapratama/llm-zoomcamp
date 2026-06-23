# Retrieval Layer

Hybrid retrieval dengan RRF fusion dan cross-encoder reranking.

## Architecture

```
User Query
    ↓
Query Rewriter (LLM) — expands abbreviations, adds regulatory context
    ↓              ↓
Vector Search    Keyword Search
(PGVector)       (PostgreSQL FTS)
    ↓              ↓
    ← RRF Fusion (k=60) →
         ↓
  Cross-Encoder Reranker (top-5)
         ↓
  Final ranked chunks → LLM
```

## Files

```
retrieval/
├── README.md
├── vector_search.py          ← PGVector cosine similarity search
├── keyword_search.py         ← PostgreSQL FTS (tsvector) search
├── rrf_fusion.py             ← Reciprocal Rank Fusion implementation
├── reranker.py               ← Cross-encoder reranking
├── query_rewriter.py         ← LLM-based query expansion
└── pipeline.py               ← Full retrieval pipeline (compose all above)
```

## RRF Formula

For each document `d` across `n` ranked lists:

```
RRF_score(d) = Σ 1 / (k + rank(d))
```

where `k=60` is the smoothing constant.

## Models

| Component | Model | Notes |
|-----------|-------|-------|
| Embeddings | `intfloat/multilingual-e5-base` | 768-dim; Bahasa Indonesia + English |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Fast; swap to Cohere Rerank for production |
