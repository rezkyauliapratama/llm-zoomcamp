# Final Project — OJK AI Regulation Q&A System

## Overview
An intelligent Q&A system for OJK (Otoritas Jasa Keuangan) AI-related regulations, built using a RAG (Retrieval-Augmented Generation) architecture. The system enables bank staff and compliance officers to query regulatory documents in natural language and receive accurate, cited answers.

## Problem Statement
OJK and Bank Indonesia are actively issuing AI governance frameworks (POJK, SEOJK, and Cetak Biru AI). Compliance teams struggle to navigate the volume of regulatory text. This system provides a conversational interface grounded in verified regulatory sources.

## Architecture
```
[Regulatory PDFs] → [Ingestion Pipeline] → [Vector Store (Qdrant/Elasticsearch)]
                                                        ↓
[User Query] → [Retrieval] → [Reranking] → [LLM Generation] → [Cited Answer]
                                                        ↓
                                              [Monitoring (Grafana/PostgreSQL)]
```

## Stack
| Component | Technology |
|---|---|
| LLM | GPT-4o / Mistral 7B (open-source fallback) |
| Vector Store | Elasticsearch / Qdrant |
| Embeddings | text-embedding-3-small / bge-m3 |
| Orchestration | Mage AI |
| Monitoring | PostgreSQL + Grafana |
| App | Streamlit |
| Containerization | Docker Compose |

## Project Structure
```
final-project/
├── data/
│   ├── raw/          # Original regulatory PDF documents
│   └── processed/    # Chunked & embedded documents
├── src/
│   ├── ingestion.py  # Document ingestion pipeline
│   ├── retrieval.py  # Vector search & hybrid retrieval
│   ├── generation.py # LLM generation with citations
│   └── evaluation.py # RAG evaluation metrics
├── notebooks/
│   ├── 01-data-exploration.ipynb
│   ├── 02-rag-baseline.ipynb
│   └── 03-evaluation.ipynb
├── app/
│   └── app.py        # Streamlit application
├── monitoring/
│   ├── docker-compose.yml
│   └── grafana/dashboard.json
├── Makefile
├── docker-compose.yml
└── requirements.txt
```

## Setup
```bash
# Clone the repo
git clone https://github.com/rezkyauliapratama/llm-zoomcamp
cd llm-zoomcamp/final-project

# Start services
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run ingestion
python src/ingestion.py

# Launch app
streamlit run app/app.py
```

## Evaluation Targets
- **Hit Rate @5**: > 0.80
- **MRR @5**: > 0.65
- **LLM-as-judge Relevance**: > 4.0/5.0
- **Answer Faithfulness**: > 0.85
- **TTFT**: < 2s

## References
- [LLM Zoomcamp — DataTalksClub](https://github.com/DataTalksClub/llm-zoomcamp)
- [OJK POJK AI Regulation](https://www.ojk.go.id)
- [BI Cetak Biru AI](https://www.bi.go.id)
