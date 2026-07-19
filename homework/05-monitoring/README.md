# Module 05 — Monitoring

Homework submission for [LLM Zoomcamp 2026 Cohort](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026/05-monitoring).

---

## Overview

This homework explores **OpenTelemetry (OTel)** for monitoring a RAG system.
We instrument the RAG pipeline with traces, capture metrics as span attributes,
persist spans to SQLite via a custom exporter, and query trace data.

Concepts covered:
- OpenTelemetry traces, spans, and attributes
- Manual code instrumentation with `start_as_current_span`
- Capturing tokens, cost, and timing as span attributes
- Custom `SpanExporter` implementation (SQLite persistence)
- Querying trace data with SQL/pandas
- Token stability analysis across runs

---

## Setup

### Prerequisites

- Python 3.12+
- uv package manager
- OpenAI API key (or any OpenAI-compatible provider)

### Installation

```bash
cp .env.template .env
# Edit .env with your API key

uv sync
```

### Download helper files

```bash
PREFIX=https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/cohorts/2026/05-monitoring
wget $PREFIX/rag_helper.py
wget $PREFIX/starter.py
```

---

## Running

```bash
uv run python homework.py
```

This runs all 6 homework questions and prints the answers. Results
are approximate and may vary between runs and models.

---

## Homework Answers

### Q1 — First trace: how many spans?

**Answer: 3**

The `RAGTraced` subclass wraps `rag()`, `search()`, and `llm()` each
in their own span. A single RAG call produces 3 spans in the trace.
Options: 1, 3, 5, 7.

### Q2 — Input tokens as span attribute

**Answer: ~700**

The LLM span captures `input_tokens` from the response usage. For a
typical query with chunked context, this is around 700-1200 tokens.
Options: 700, 7000, 70000, 700000.

### Q3 — Span timing (LLM call duration)

**Answer: 500-2000ms**

The LLM call typically takes between 500ms and 2000ms for a model
like GPT-5.4-mini. First calls can be slower due to cold start.
Options: Under 100ms, 100-500ms, 500-2000ms, Over 2000ms.

### Q4 — Span names in SQLite

**Answer: rag, search, and llm**

The custom `SQLiteSpanExporter` persists all 3 spans to the `spans`
table. Each span name appears as a row.
Options: Only `rag` | `rag` and `llm` | `rag`, `search`, and `llm` |
`search`, `llm`, and `judge`.

### Q5 — Total duration by span type

**Answer: llm**

Excluding the parent `rag` span, the `llm` span takes the most total
time because the API call dominates the RAG pipeline vs. local search.
Options: `search` | `llm` | They're all about the same.

### Q6 — Token stability across runs

**Answer: Within 10% of each other**

The input tokens are relatively stable across runs because the search
retrieves the same documents for the same query, producing a consistent
context window. Small variations may occur due to search ordering.
Options: They're identical | Within 10% | Within 50% | Vary more than 50%.

---

## File Structure

```
homework/05-monitoring/
├── .env.template       # copy to .env and fill in OPENAI_API_KEY
├── .gitignore          # standard ignores + *.db
├── pyproject.toml      # uv project config with OTel dependencies
├── rag_helper.py       # RAGBase class (from DataTalksClub starter)
├── starter.py          # Loads course docs, builds index, creates RAG
├── homework.py         # Main script — Q1 through Q6 with OTel
└── README.md           # this file
```

---

## References

- [Homework instructions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/05-monitoring/homework.md)
- [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [gitsource](https://github.com/alexeygrigorev/gitsource)
- [minsearch](https://github.com/alexeygrigorev/minsearch)
