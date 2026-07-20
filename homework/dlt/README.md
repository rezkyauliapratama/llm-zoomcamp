# dlt + Logfire Workshop Homework

Homework submission for [dlt Workshop](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026/workshops/dlt).

---

## Overview

Take the FAQ agent from Module 1, rewrite it with **Pydantic AI**,
instrument it with **Pydantic Logfire** for observability, then pull
the trace data back out with **dlt** into **DuckDB** for analysis.

This bridges two course modules:
- Module 1 (Agentic RAG): the FAQ agent concept
- Module 5 (Monitoring): observability and tracing

Concepts covered:
- Pydantic AI agents (declarative agent with tool registration)
- Logfire instrumentation (`logfire.instrument_pydantic_ai()`)
- Trace spans, attributes, and token usage
- dlt pipeline from Logfire source to DuckDB
- Auto-normalization of nested trace JSON

---

## Prerequisites

- Python 3.11+
- uv package manager
- OpenAI API key (or any OpenAI-compatible provider)
- **Free Logfire account** at [logfire.dev](https://logfire.dev)

---

## Setup

### 1. Install dependencies

```bash
cp .env.template .env
# Edit .env with your OPENAI_API_KEY

uv sync
```

### 2. Verify the agent runs

```bash
uv run python main.py
```

This downloads the DataTalks.Club FAQ, builds a minsearch index, and
runs the Pydantic AI FAQ agent with the question "I just discovered
the course. Can I join it?"

---

## Homework Answers

### Q1 — Instrument with Logfire: how many spans?

**Answer: 15**

Sign up at [logfire.dev](https://logfire.dev), create a project, get a
write token. Add to `.env` as `LOGFIRE_TOKEN`. Then instrument:

```python
import logfire
logfire.configure()
logfire.instrument_pydantic_ai()
```

Run the query "How do I run Ollama locally?" and count spans in the
Logfire dashboard. Each span is an agent run, an LLM call, or a tool
call. Number varies by how many searches the agent makes.

Options: 1, 5, 15, 30.

### Q2 — dlt into DuckDB: how many tables?

**Answer: 24**

Generate a read token from Logfire and set as `LOGFIRE_READ_TOKEN`. Use
dlt's Logfire source to pull traces into DuckDB. dlt auto-normalizes
deeply nested trace JSON into a main table + child tables for each
nested level (span attributes, LLM messages, tool calls, token usage).

Check with:
```sql
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'agent_traces';
```

Options: 1, 3, 24, 100.

### Q3 — Total input token usage

**Answer: 1500-5000**

Token counts are stored in span attributes as `gen_ai.usage.input_tokens`.
Sum across all LLM calls within the trace. The number depends on how
many searches the agent made. For a typical run with 2-3 search calls,
expect ~1500-5000 input tokens.

Options: 100-500 | 1500-5000 | 10000-20000 | 50000-100000.

---

## Project Structure

```
homework/dlt/
├── .env.template    # API keys template
├── .gitignore       # standard + *.duckdb
├── pyproject.toml   # uv project config
├── ingest.py        # Download FAQ + build minsearch index
├── agent.py         # Pydantic AI FAQ agent (search tool)
├── main.py          # Entry point — run the agent
├── homework.py      # Q1-Q3 solution script
└── README.md        # this file
```

---

## References

- [Homework instructions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/workshops/dlt/homework.md)
- [dltHub Logfire context](https://dlthub.com/context/source/logfire)
- [Pydantic AI docs](https://ai.pydantic.dev/)
- [Logfire docs](https://logfire.dev/docs)
- [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
