# Final Project — OJK Regulatory Document Q&A System

## Overview
An intelligent Q&A system for OJK (Otoritas Jasa Keuangan) regulatory documents, enabling bank compliance teams to query regulations in natural language.

## Problem Statement
Bank compliance officers spend significant time manually searching through OJK regulations (POJK, SEOJK, circulars). This system provides instant, accurate answers grounded in official regulatory documents.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                  (Streamlit / FastAPI)                   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   RAG Pipeline                           │
│  Query → Embedding → Vector Search → Rerank → LLM       │
└──────┬───────────────────────────────────────┬──────────┘
       │                                       │
┌──────▼──────┐                    ┌───────────▼──────────┐
│  Vector DB  │                    │      LLM (OpenAI /   │
│(Elasticsearch│                   │    open-source)       │
│  / Qdrant)  │                    └──────────────────────┘
└─────────────┘
```

## Dataset
- OJK regulatory documents (POJK, SEOJK)
- Source: [ojk.go.id](https://www.ojk.go.id)
- Format: PDF → chunked text

## Tech Stack
- **LLM**: OpenAI GPT-4o / Ollama (Mistral/Llama3)
- **Embeddings**: `text-embedding-3-small` / `sentence-transformers`
- **Vector Store**: Elasticsearch / Qdrant
- **Orchestration**: Mage AI / Prefect
- **Monitoring**: Grafana + PostgreSQL
- **UI**: Streamlit
- **Containerization**: Docker Compose

## Project Structure
```
final-project/
├── data/
│   ├── raw/              # Raw OJK PDFs
│   └── processed/        # Chunked & cleaned text
├── ingestion/
│   ├── pdf_parser.py     # PDF extraction
│   ├── chunker.py        # Document chunking
│   └── indexer.py        # Vector DB indexing
├── rag/
│   ├── retriever.py      # Search & retrieval
│   ├── reranker.py       # Reranking logic
│   └── generator.py      # LLM answer generation
├── evaluation/
│   ├── generate_gt.py    # Ground truth generation
│   └── evaluate.py       # RAG evaluation metrics
├── monitoring/
│   ├── grafana/          # Grafana dashboards
│   └── postgres_init.sql # DB schema for monitoring
├── app/
│   └── app.py            # Streamlit UI
├── notebooks/
│   └── exploration.ipynb # EDA & prototyping
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Evaluation Metrics
- **Retrieval**: Hit Rate @5, MRR @5
- **Generation**: LLM-as-judge (relevance, faithfulness, completeness)
- **Latency**: TTFT < 2s, end-to-end < 5s

## Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run with Docker
```bash
docker-compose up -d
```

### Start the App
```bash
streamlit run app/app.py
```

## References
- [LLM Zoomcamp Final Project Guidelines](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/project.md)
- [OJK Official Website](https://www.ojk.go.id)
