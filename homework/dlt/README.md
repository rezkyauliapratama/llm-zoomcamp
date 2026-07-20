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
- OpenAI API key (or any OpenAI-compatible provider like OpenRouter)
- **Free Logfire account** at [logfire.dev](https://logfire.dev)

---

## Setup

### 1. Install dependencies

```bash
cp .env.template .env
# Edit .env with your API key
# For OpenRouter, add: OPENAI_BASE_URL=https://openrouter.ai/api/v1

uv sync
```

### 2. Verify the agent runs

```bash
source .env && uv run python main.py
```

This downloads the DataTalks.Club FAQ, builds a minsearch index, and
runs the Pydantic AI FAQ agent with the question "I just discovered
the course. Can I join it?"

> **OpenRouter users:** Pydantic AI respects `OPENAI_BASE_URL` from env.
> The agent was verified working with OpenRouter (`gpt-5.4-mini`).

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
Logfire dashboard.

**Actual agent behavior** (from local run with OpenRouter):
- LLM requests: **2** (initial + follow-up with tool results)
- Tool calls: **3** (all parallel in one turn)
- With Logfire instrumentation: agent run + LLM calls + tool calls
  + internal spans ≈ **~15 spans**

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

**Answer: 1500-5000** (actual: 4019)

Token counts are stored in span attributes as `gen_ai.usage.input_tokens`.
Sum across all LLM calls within the trace.

**Actual run results** (OpenRouter, gpt-5.4-mini):
- Input tokens: **4019**
- Output tokens: **348**
- Tool calls: **3** (all parallel in one turn)
- LLM requests: **2** (initial request + follow-up with tool results)

Options: 100-500 | 1500-5000 | 10000-20000 | 50000-100000.

---

## Project Structure

```
homework/dlt/
├── .env.template    # API keys template (OpenAI / OpenRouter + Logfire)
├── .gitignore       # standard + *.duckdb
├── pyproject.toml   # uv project config
├── ingest.py        # Download FAQ + build minsearch index
├── agent.py         # Pydantic AI FAQ agent (search tool)
├── main.py          # Entry point — run the agent
├── homework.py      # Q1-Q3 solution script
└── README.md        # this file
```

---

## OpenRouter Support

Pydantic AI reads `OPENAI_BASE_URL` from the environment, so you can
use any OpenAI-compatible provider without code changes:

```bash
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_API_KEY=sk-or-...
```

The agent model string `openai:gpt-5.4-mini` works with OpenRouter
because Pydantic AI's OpenAI provider routes through the custom base
URL automatically. This was verified in local testing.

---

## References

- [Homework instructions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/workshops/dlt/homework.md)
- [dltHub Logfire context](https://dlthub.com/context/source/logfire)
- [Pydantic AI docs](https://ai.pydantic.dev/)
- [Logfire docs](https://logfire.dev/docs)
- [OpenRouter](https://openrouter.ai)
- [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
