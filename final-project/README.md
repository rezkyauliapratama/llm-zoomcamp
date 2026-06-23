# Final Project: OJK/BI Regulatory Intelligence Assistant

> **LLM Zoomcamp 2026 — Final Project**
> **Author:** Rezky Aulia Pratama | Solution Architect, PT Bank Sinarmas Tbk

---

## ⚠️ Disclaimer

This is a personal learning project (LLM Zoomcamp 2026 Final Project).
Not affiliated with PT Bank Sinarmas Tbk or any financial institution.
All documents sourced from [ojk.go.id](https://ojk.go.id) and [bi.go.id](https://bi.go.id) are public domain
under Indonesian Copyright Law No. 28/2014, Article 42.
Not legal advice — always verify with original source documents.

---

## Problem Statement

Compliance, legal, and risk management teams at Indonesian banks spend significant manual effort searching through hundreds of pages of OJK and Bank Indonesia regulatory documents (POJK, SE OJK, PBI, PADG) every time a policy question arises. A single POJK document can exceed 100 pages, and regulation volumes grow every year.

This project builds an **end-to-end RAG application** that answers natural language questions about Indonesian banking regulations in seconds, with explicit citations to the source document and pasal (article).

### Example Questions
- "Apa kewajiban bank terkait tata kelola kecerdasan artifisial berdasarkan panduan OJK 2025?"
- "Berapa batas minimum modal inti bank umum konvensional?"
- "What are the key principles of model risk management under OJK's AI governance framework?"
- "Sebutkan persyaratan manajemen risiko teknologi informasi untuk bank berdasarkan POJK terbaru"

---

## Architecture

```
┌─────────────────────────────────────┐
│     INGESTION PIPELINE (N8N)        │
│  Schedule → Fetch PDF → Chunk →     │
│  Embed → PGVector Store             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         RETRIEVAL LAYER             │
│  Query Rewriter → Vector Search     │
│  + Keyword Search → RRF Fusion →    │
│  Cross-Encoder Reranker             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      GENERATION LAYER (LLM)         │
│  System Prompt + Context → LLM →    │
│  Answer with pasal citations        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    INTERFACE (Open WebUI)           │
│  Chat + Citations + Feedback        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    MONITORING (Grafana)             │
│  5+ dashboard charts                │
└─────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Tool |
|-------|------|
| Chat Interface | Open WebUI |
| Ingestion Pipeline | N8N |
| Vector Store | PostgreSQL + pgvector |
| Embeddings | `intfloat/multilingual-e5-base` (768-dim) |
| Keyword Search | PostgreSQL FTS (tsvector) |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| LLM | TBD (OpenAI / Groq / Ollama / AWS Bedrock) |
| Monitoring | Grafana |
| Containerization | Docker Compose |
| Cloud Deployment (Bonus) | GCP Cloud Run + Cloud SQL |

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/rezkyauliapratama/llm-zoomcamp
cd llm-zoomcamp/final-project

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up -d

# Access services
# Open WebUI:  http://localhost:3000
# N8N:         http://localhost:5678
# Grafana:     http://localhost:3001
# PostgreSQL:  localhost:5432
```

---

## Project Structure

```
final-project/
├── README.md                    ← this file
├── .env.example                 ← environment variables template
├── docker-compose.yaml          ← all 4 services
├── ingestion/                   ← document ingestion pipeline
├── retrieval/                   ← retrieval & reranking logic
├── evaluation/                  ← retrieval + LLM evaluation
├── monitoring/                  ← Grafana dashboard + SQL schema
├── notebooks/                   ← exploratory notebooks
└── docs/                        ← additional documentation
```

---

## Evaluation Criteria

Target score: **23/22** (all base + all bonuses)

| Criteria | Target | Status |
|----------|--------|--------|
| Problem description | 2/2 | ✅ |
| Retrieval flow | 2/2 | ⏳ |
| Retrieval evaluation | 2/2 | ⏳ |
| LLM evaluation | 2/2 | ⏳ |
| Interface | 2/2 | ⏳ |
| Ingestion pipeline | 2/2 | ⏳ |
| Monitoring | 2/2 | ⏳ |
| Containerization | 2/2 | ⏳ |
| Reproducibility | 2/2 | ⏳ |
| Hybrid search (bonus) | 1/1 | ⏳ |
| Reranking (bonus) | 1/1 | ⏳ |
| Query rewriting (bonus) | 1/1 | ⏳ |
| Cloud deployment (bonus) | 2/2 | ⏳ |
