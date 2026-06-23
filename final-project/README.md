# LLM Zoomcamp — Final Project

## Project: OJK Regulatory Intelligence Assistant

An end-to-end RAG-based AI assistant to help navigate OJK (Otoritas Jasa Keuangan) and Bank Indonesia regulatory documents for financial services compliance in Indonesia.

## Problem Statement

Financial institutions in Indonesia must navigate a complex and frequently updated regulatory landscape from OJK and Bank Indonesia. Compliance teams spend significant time manually searching through hundreds of regulations to find relevant rules, circulars, and guidelines. This project builds an intelligent assistant that can retrieve and synthesize regulatory information accurately.

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    RAG Pipeline (LangChain)                     │
│  ┌─────────────┐   ┌──────────────┐   ┌───────────────────┐    │
│  │  Query      │──▶│  Retrieval   │──▶│  LLM Generation  │    │
│  │  Rewriting  │   │  (Hybrid)    │   │  (GPT-4o / OSS)  │    │
│  └─────────────┘   └──────────────┘   └───────────────────┘    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    Knowledge Base                               │
│  ┌─────────────────────┐    ┌──────────────────────────────┐   │
│  │  Vector DB (Qdrant) │    │  Elasticsearch (BM25)        │   │
│  │  - OJK Regulations  │    │  - Full-text keyword search  │   │
│  │  - BI Circulars     │    │                              │   │
│  └─────────────────────┘    └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
final-project/
├── README.md                    # This file
├── data/                        # Raw and processed regulatory documents
│   ├── raw/                     # Original PDF/HTML files
│   └── processed/               # Chunked and cleaned documents
├── notebooks/                   # Exploration and prototyping notebooks
│   ├── 01-data-exploration.ipynb
│   ├── 02-indexing-pipeline.ipynb
│   └── 03-evaluation.ipynb
├── src/                         # Source code
│   ├── ingestion/               # Document ingestion and preprocessing
│   │   ├── __init__.py
│   │   ├── loader.py            # Document loaders (PDF, HTML)
│   │   ├── chunker.py           # Chunking strategies
│   │   └── embedder.py          # Embedding generation
│   ├── retrieval/               # Retrieval logic
│   │   ├── __init__.py
│   │   ├── vector_store.py      # Qdrant integration
│   │   ├── keyword_search.py    # Elasticsearch integration
│   │   └── hybrid.py            # Hybrid search + reranking
│   ├── generation/              # LLM generation
│   │   ├── __init__.py
│   │   ├── prompts.py           # Prompt templates
│   │   └── llm.py               # LLM client wrapper
│   └── evaluation/              # Evaluation pipeline
│       ├── __init__.py
│       ├── metrics.py           # Hit rate, MRR, NDCG
│       └── judge.py             # LLM-as-a-judge
├── app/                         # Streamlit application
│   ├── app.py                   # Main Streamlit app
│   └── components/              # Reusable UI components
├── pipeline/                    # Orchestration (Mage/Prefect)
│   └── ingestion_pipeline.py
├── evaluation/                  # Evaluation results
│   ├── ground_truth.csv         # Ground truth QA pairs
│   └── results/                 # Evaluation run results
├── docker/                      # Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── .env.example                 # Environment variable template
└── Makefile                     # Common commands
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| **LLM** | GPT-4o / Llama 3 (via Ollama) |
| **Embeddings** | `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` |
| **Vector DB** | Qdrant |
| **Keyword Search** | Elasticsearch |
| **RAG Framework** | LangChain |
| **Orchestration** | Mage AI |
| **UI** | Streamlit |
| **Evaluation** | Custom + LLM-as-a-Judge |
| **Monitoring** | Grafana + PostgreSQL |
| **Containerization** | Docker Compose |

## Evaluation Strategy

- **Retrieval**: Hit Rate @5, MRR @5
- **Generation**: LLM-as-a-Judge (relevance, faithfulness, completeness)
- **Ground truth**: 100 QA pairs generated from OJK/BI documents
- **Target**: Hit Rate > 0.80, Faithfulness Score > 4.0/5.0

## Getting Started

```bash
# Clone and setup
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/final-project

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Start infrastructure
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run ingestion pipeline
python pipeline/ingestion_pipeline.py

# Launch app
streamlit run app/app.py
```

## References

- [LLM Zoomcamp Final Project Guidelines](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/project)
- [OJK Official Regulations](https://www.ojk.go.id/id/regulasi)
- [Bank Indonesia Regulations](https://www.bi.go.id/id/publikasi/peraturan)
