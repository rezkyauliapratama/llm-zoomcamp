# 🧠 LLM Zoomcamp 2026 — Rezky Aulia Pratama

> **Course:** [LLM Zoomcamp 2026](https://github.com/DataTalksClub/llm-zoomcamp) by DataTalks.Club  
> **Status:** In Progress

---

## ⚠️ Disclaimer

This is a **personal learning project** for LLM Zoomcamp 2026.  
Not affiliated with any financial institution.  
All documents sourced from `ojk.go.id` and `bi.go.id` are public domain under Indonesian Copyright Law No. 28/2014, Article 42.  
Not legal advice — always verify with original source documents.

---

## 📁 Repository Structure

```
llm-zoomcamp/
└── homework/
    ├── 01-agentic-rag/          # Module 01 — Agentic RAG
    ├── 02-vector-search/        # Module 02 — Vector Search
    ├── 03-orchestration/        # Module 03 — AI Orchestration
    ├── 04-evaluation/           # Module 04 — Evaluation
    ├── 05-monitoring/           # Module 05 — Monitoring (OTel)
    ├── dlt/                     # Workshop — dlt + Logfire
    └── ...
```

---

## 📚 Modules & Homework

| Module | Title | Homework | Status |
|--------|-------|----------|--------|
| 01 | Agentic RAG | [homework/01-agentic-rag](./homework/01-agentic-rag/) | ✅ Done |
| 02 | Vector Search | [homework/02-vector-search](./homework/02-vector-search/) | ✅ Done |
| 03 | AI Orchestration (Kestra) | [homework/03-orchestration](./homework/03-orchestration/) | ✅ Done |
| 04 | Evaluation | [homework/04-evaluation](./homework/04-evaluation/) | ✅ Done |
| 05 | Monitoring | [homework/05-monitoring](./homework/05-monitoring/) | ✅ Done |
| — | dlt Workshop | [homework/dlt](./homework/dlt/) | ✅ Done |
| 06 | TBD | TBD | ⏳ Pending |
| 07 | TBD | TBD | ⏳ Pending |
| 08 | TBD | TBD | ⏳ Pending |

---

## 📖 Module Highlights

### Module 02 — Vector Search

Tech stack: **Python 3.11+**, **uv**, **Cohere Embedding**

| File | Description |
|------|-------------|
| `download.py` | Download and prepare course documents |
| `embedder.py` | Generate embeddings using Cohere API |
| `homework.py` | Homework answers — vector search with SQLite, pgvector |
| `pyproject.toml` | uv project configuration |

### Module 03 — AI Orchestration with Kestra

Tech stack: **Kestra v1.3.21**, **PostgreSQL 18**, **Docker Compose**

| Flow | Provider | Description |
|------|----------|-------------|
| `1_chat_without_rag.yaml` | Gemini 2.5 Flash | Query Kestra features without RAG |
| `2_chat_with_rag.yaml` | Gemini 2.5 Flash + Embeddings | RAG with Kestra release docs |
| `3_rag_with_websearch.yaml` | **OpenRouter (GPT-5 Mini)** | RAG + live web search via Tavily |
| `4_simple_agent.yaml` | Gemini 2.5 Flash | Multi-language summary agent |
| `5_web_research_agent.yaml` | Gemini 2.5 Flash + Tavily | Autonomous web research agent |
| `6_multi_agent_research.yaml` | Gemini 2.5 Flash | Multi-agent company research |

> Flow 3 uses OpenRouter (`io.kestra.plugin.ai.provider.OpenRouter`) with OpenAI-compatible endpoint, model `openai/gpt-5-mini`, and Tavily web search.

### Module 04 — Evaluation

Tech stack: **Python 3.12+**, **uv**, **OpenAI**, **minsearch**, **gitsource**

| File | Description |
|------|-------------|
| `homework.py` | Full evaluation pipeline — Q1 to Q6 |
| `ground-truth.csv` | 360 labeled questions across 72 course pages |
| `pyproject.toml` | uv project configuration |

### Module 05 — Monitoring (OpenTelemetry)

Tech stack: **Python 3.12+**, **uv**, **OpenTelemetry**, **SQLite**, **minsearch**

| File | Description |
|------|-------------|
| `rag_helper.py` | RAGBase class (from course starter) |
| `starter.py` | Loads course docs, builds text-search index, creates RAG instance |
| `homework.py` | OTel instrumentation — traces, span attributes, SQLite exporter, Q1-Q6 |
| `pyproject.toml` | uv project config with opentelemetry-api, opentelemetry-sdk |

Concepts covered:
- OpenTelemetry traces, spans, and attributes
- Manual code instrumentation with `start_as_current_span`
- Custom `SpanExporter` (SQLite persistence)
- Token/cost capture as span attributes
- Trace data querying with pandas
- Token stability analysis

### dlt Workshop — Pydantic AI + Logfire + dlt

Tech stack: **Python 3.11+**, **uv**, **Pydantic AI**, **Logfire**, **dlt**, **DuckDB**

| File | Description |
|------|-------------|
| `agent.py` | Pydantic AI FAQ agent with search tool |
| `ingest.py` | Download DataTalks.Club FAQ + build minsearch index |
| `main.py` | Entry point — run the agent |
| `homework.py` | Q1-Q3 — Logfire instrumentation, dlt pipeline, token analysis |
| `pyproject.toml` | uv project config with pydantic-ai, logfire |

Concepts covered:
- Pydantic AI agents (declarative tool registration)
- Logfire instrumentation for observability
- Trace spans and attributes (LLM calls, tool calls)
- dlt pipeline from Logfire source to DuckDB
- Auto-normalization of nested trace JSON

---

## 🔗 References

- [DataTalksClub/llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
- [Course Cohort 2026](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Pydantic AI](https://ai.pydantic.dev/)
- [Logfire](https://logfire.dev)
- [dltHub](https://dlthub.com)
