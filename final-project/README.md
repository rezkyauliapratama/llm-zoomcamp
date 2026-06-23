# OJK/BI Regulatory Intelligence Assistant

> **LLM Zoomcamp 2026 — Final Project**  
> Target Score: **23/22** (all base points + all bonuses)

## Problem Statement

Compliance and risk management teams at Indonesian banks spend significant manual effort searching through hundreds of pages of OJK and Bank Indonesia regulatory documents (POJK, SE OJK, PBI, PADG). A single POJK document can exceed 100 pages, and regulation volumes grow every year.

This project builds an **end-to-end RAG application** that answers natural language questions about Indonesian banking regulations in seconds, with explicit citations to source documents and *pasal* (articles).

## Example Questions

- *"Apa kewajiban bank terkait tata kelola kecerdasan artifisial berdasarkan panduan OJK 2025?"*
- *"Berapa batas minimum modal inti bank umum konvensional?"*
- *"What are the key principles of model risk management under OJK's AI governance framework?"*

## Architecture

```
[N8N Ingestion Pipeline]
    PDF Download (ojk.go.id / bi.go.id)
    → Text Extraction (Apache Tika)
    → Section-Based Chunking (BAB/Pasal aware)
    → Metadata Enrichment
    → multilingual-e5-base Embeddings
    → PGVector Store

[Retrieval Layer]
    User Query
    → Query Rewriter (LLM)
    → Hybrid Search: PGVector (dense) + PostgreSQL FTS (sparse)
    → RRF Fusion
    → Cross-Encoder Reranker (top-5)

[Generation Layer]
    System Prompt V1 or V2 + Retrieved Chunks + Query
    → LLM (OpenAI / Groq / Ollama / AWS Bedrock)
    → Answer with pasal citations
    → Log to PostgreSQL conversations table

[Interface]
    Open WebUI — Chat UI with citation panel + feedback

[Monitoring]
    Grafana — 5+ dashboard charts from PostgreSQL logs
```

## Evaluation Criteria Status

| Criteria | Points | Status |
|----------|--------|--------|
| Problem description | 2/2 | ✅ Defined |
| Retrieval flow | 2/2 | ⏳ Building |
| Retrieval evaluation | 2/2 | ⏳ Pending |
| LLM evaluation | 2/2 | ⏳ Pending |
| Interface | 2/2 | ⏳ Pending |
| Ingestion pipeline | 2/2 | ⏳ Pending |
| Monitoring | 2/2 | ⏳ Pending |
| Containerization | 2/2 | ⏳ Pending |
| Reproducibility | 2/2 | ⏳ Pending |
| Hybrid search (bonus) | 1/1 | ⏳ Planned |
| Reranking (bonus) | 1/1 | ⏳ Planned |
| Query rewriting (bonus) | 1/1 | ⏳ Planned |
| Cloud deployment (bonus) | 2/2 | ⏳ Planned (GCP) |

## Quick Start

```bash
# Clone and setup
git clone https://github.com/rezkyauliapratama/llm-zoomcamp
cd llm-zoomcamp/final-project

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker compose up -d

# Run data ingestion
python ingestion/scripts/ingest_all.py

# Access services
# Open WebUI:  http://localhost:3000
# N8N:         http://localhost:5678
# Grafana:     http://localhost:3001
```

## Services (Docker Compose)

| Service | Port | Description |
|---------|------|-------------|
| open-webui | 3000 | Chat interface |
| n8n | 5678 | Ingestion pipeline orchestration |
| postgres-pgvector | 5432 | Vector store + conversation logging |
| grafana | 3001 | Monitoring dashboard |

## Dataset & Legal Notice

All documents sourced from `ojk.go.id` and `bi.go.id` are **public domain** under Indonesian Copyright Law No. 28/2014, Article 42 (government regulatory documents are excluded from copyright protection).

> **Disclaimer:** This is a personal learning project (LLM Zoomcamp 2026 Final Project). Not affiliated with any financial institution. Not legal advice — always verify with original source documents.

## References

- [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp)
- [OJK Official Website](https://ojk.go.id)
- [Bank Indonesia Official Website](https://bi.go.id)
