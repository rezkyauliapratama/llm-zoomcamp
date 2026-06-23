# Architecture Documentation

## System Overview

The OJK/BI Regulatory Intelligence Assistant is a production-grade RAG system
designed for Indonesian banking compliance teams.

## Component Details

### 1. Ingestion Pipeline (N8N)

N8N orchestrates the weekly ingestion of regulatory documents:

1. **Schedule Trigger** — runs every Sunday at 02:00 WIB
2. **HTTP Request nodes** — download PDFs from ojk.go.id and bi.go.id
3. **Extract from File** — N8N built-in PDF text extraction
4. **Recursive Character Text Splitter** — chunk_size=512, overlap=64
5. **Metadata Enrichment** — source_document, pasal, bab, tahun, topik, bahasa
6. **Embeddings** — multilingual-e5-base (768-dim)
7. **PGVector Store** — insert mode, HNSW index

### 2. Retrieval Layer

Hybrid search pipeline:

```
User Query
  → Query Rewriter (LLM)
  → [Vector Search (PGVector)] + [Keyword Search (PostgreSQL FTS)]
  → RRF Fusion (k=60)
  → Cross-Encoder Reranker → top-5 chunks
```

**Chunking Strategy** (Section-Based, Legal Document Optimized):
- Detect BAB headings (e.g., "BAB III - MANAJEMEN RISIKO")
- Detect Pasal headings (e.g., "Pasal 15", "Pasal 15 Ayat 2")
- Chunk at Pasal level — each pasal = one or more chunks
- Target: 400–600 tokens per chunk, 50–100 token overlap at section boundaries

### 3. Generation Layer

**Prompt V1** (Strict Citation):
> Answer ONLY from context. Cite every claim: [Sumber: {doc}, {pasal}].
> If not in context, say: "Tidak ditemukan dalam dokumen regulasi yang tersedia."

**Prompt V2** (Structured Response):
> 1. Direct answer, 2. Numbered points with citations, 3. Reference list.

### 4. Interface Layer (Open WebUI)

- Chat interface with citation panel
- Feedback widget (thumbs up/down)
- Knowledge Base workspace for admin uploads
- Custom model with system prompt attached

### 5. Monitoring Layer (Grafana)

5 required charts + 3 optional charts.
All data flows through `conversations` table in PostgreSQL.

## N8N ↔ Open WebUI Integration

**Phase 1 (MVP):** N8N ingestion-only → Open WebUI native RAG

**Phase 2 (Full Control):** N8N full RAG pipeline → Open WebUI via Pipeline Function

## Security Considerations

- All secrets in `.env` (never committed)
- GCP: Secret Manager for production credentials
- Database: separate schemas for vector store and monitoring
- Network: docker internal network, only necessary ports exposed
