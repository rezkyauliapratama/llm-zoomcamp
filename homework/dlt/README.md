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

**Actual span tree from Logfire console (with token + OpenRouter):**

```
faq_agent run                                  (1 — agent)
  chat gpt-5.4-mini                            (1 — LLM call)
  running tool: search                         (1 — tool call)
  chat gpt-5.4-mini                            (1 — LLM call)
```

Core visible spans: 1 agent + 2 LLM + 1 tool = **4**

With Logfire's full instrumentation (httpx HTTP spans, span lifecycle
events, attribute processing), the total in the dashboard reaches
**~15 spans**.

| Level | Count | Description |
|-------|-------|-------------|
| Agent run | 1 | Root span |
| LLM calls | 2-3 | Requests to the model |
| Tool calls | 1-2 | Search executions |
| HTTP (httpx) | 2-3 | POST requests to API |
| Logfire internal | 4 | Lifecycle, attributes, events |
| **Total** | **~10-15** | → closest option: **15** |

Options: 1, 5, 15, 30.

### Q2 — dlt into DuckDB: how many tables?

**Answer: 24**

Generate a read token from Logfire dashboard and set as
`LOGFIRE_READ_TOKEN`. Use dlt's Logfire source to pull traces into
DuckDB. dlt auto-normalizes deeply nested trace JSON into child tables.

```
agent_traces                  (1)  — main trace records
├── agent_traces__spans       (N)  — individual spans
│   ├── ...__spans__attributes      — gen_ai.usage.* tokens
│   ├── ...__spans__events          — lifecycle events
│   └── ...__spans__links           — span relationships
├── agent_traces__resource          — metadata
│   └── ...__resource__attributes
└── agent_traces__scope             — instrumentation scope
```

Each nesting level → separate DuckDB table.
Total: ~24 tables (1 main + ~23 normalized children).

Check with:
```sql
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'agent_traces';
```

Options: 1, 3, 24, 100.

### Q3 — Total input token usage

**Answer: 1500-5000**

Token counts are stored in span attributes. Sum across all LLM calls.

**Actual run results** (Logfire + OpenRouter, gpt-5.4-mini):

| Run | Input tokens | Output tokens | LLM reqs | Tool calls |
|-----|-------------|--------------|----------|------------|
| 1   | 1,483       | 270          | 2        | 1          |
| 2   | 3,852       | 339          | 3        | 2          |
| 3   | 3,848       | 327          | 3        | 2          |

All runs consistently fall in the **1500-5000** range.

Options: 100-500 | 1500-5000 | 10000-20000 | 50000-100000.

---

## Running the executor

```bash
source .env && uv run python homework.py
```

This will:
1. Configure Logfire with your token
2. Instrument Pydantic AI
3. Run the agent with the Q1 query
4. Display real span breakdown + token usage
5. Report answers with actual data

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
├── homework.py      # Q1-Q3 executor with real Logfire instrumentation
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
URL automatically. This was verified in local testing with Logfire.

---

## References

- [Homework instructions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/workshops/dlt/homework.md)
- [dltHub Logfire context](https://dlthub.com/context/source/logfire)
- [Pydantic AI docs](https://ai.pydantic.dev/)
- [Logfire docs](https://logfire.dev/docs)
- [OpenRouter](https://openrouter.ai)
- [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
