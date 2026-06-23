# LLM Zoomcamp — Final Project

## Project Title
**OJK Regulatory Q&A Assistant** — RAG-based intelligent assistant for Indonesian financial regulation (OJK/BI)

## Problem Statement
Navigating OJK (Otoritas Jasa Keuangan) and Bank Indonesia regulatory documents is time-consuming for compliance teams and banking professionals. This project builds a production-grade RAG system that allows users to query regulatory documents in natural language.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│              (Streamlit / FastAPI)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  RAG Pipeline                           │
│  Query → Retrieval → Reranking → Generation → Response  │
└──────┬──────────────────────────────────────┬───────────┘
       │                                      │
┌──────▼──────┐                    ┌──────────▼──────────┐
│  Vector DB  │                    │     LLM Backend     │
│ (Elasticsearch│                  │  (OpenAI / Ollama)  │
│  / pgvector)│                    └─────────────────────┘
└─────────────┘
```

## Tech Stack
| Component | Technology |
|-----------|------------|
| Embedding Model | `text-embedding-3-small` / `BAAI/bge-m3` |
| Vector Store | Elasticsearch / pgvector |
| LLM | GPT-4o-mini / Llama 3 (Ollama) |
| Orchestration | Mage AI / Prefect |
| Monitoring | Grafana + Prometheus |
| UI | Streamlit |
| Containerization | Docker Compose |

## Dataset
- OJK POJK (Peraturan OJK) documents
- Bank Indonesia circulars and regulations
- SEOJK (Surat Edaran OJK) documents

## Evaluation Metrics
- Hit Rate & MRR (retrieval quality)
- ROUGE-L / cosine similarity (answer quality)
- LLM-as-judge scoring
- Latency P50/P95/P99

## Folder Structure

```
final-project/
├── data/                    # Raw & processed regulatory documents
│   ├── raw/                 # Original PDFs / text files
│   └── processed/           # Chunked & indexed documents
├── ingestion/               # Data ingestion & indexing pipeline
│   ├── chunking.py
│   ├── embeddings.py
│   └── indexing.py
├── retrieval/               # Retrieval & reranking logic
│   ├── search.py
│   └── reranker.py
├── generation/              # LLM generation & prompt templates
│   ├── prompts.py
│   └── llm_client.py
├── evaluation/              # Evaluation scripts
│   ├── generate_ground_truth.py
│   └── evaluate.py
├── monitoring/              # Grafana dashboards & metrics
│   ├── grafana/
│   └── prometheus/
├── app/                     # Streamlit UI
│   └── streamlit_app.py
├── notebooks/               # Exploration & prototyping
├── docker-compose.yml       # Full stack deployment
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

```bash
# Clone and setup
git clone https://github.com/rezkyauliapratama/llm-zoomcamp
cd llm-zoomcamp/final-project

# Start services
docker-compose up -d

# Run ingestion pipeline
python ingestion/indexing.py

# Launch UI
streamlit run app/streamlit_app.py
```

## References
- [LLM Zoomcamp Course](https://github.com/DataTalksClub/llm-zoomcamp)
- [OJK Official Website](https://www.ojk.go.id)
- [Bank Indonesia Regulations](https://www.bi.go.id)
