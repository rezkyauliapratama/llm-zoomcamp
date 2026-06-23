# Homework 01 — Agentic RAG

> **LLM Zoomcamp 2026 · Module 1**

This solution builds a RAG system from scratch using the LLM Zoomcamp course lessons as the knowledge base, then makes it agentic with function calling.

## Overview

| | |
|---|---|
| **Dataset** | DataTalksClub/llm-zoomcamp lessons (commit `8c1834d`) |
| **Search** | [`minsearch`](https://github.com/alexeygrigorev/minsearch) (in-memory, keyword + text) |
| **LLM** | DeepSeek V3 via [OpenRouter](https://openrouter.ai) |
| **Agent** | Hand-written OpenAI tool-calling loop |

## Questions Covered

| Q | Topic |
|---|-------|
| Q1 | Count lesson pages in the dataset |
| Q2 | Index with minsearch and search |
| Q3 | RAG pipeline + measure input tokens |
| Q4 | Chunk documents (size=2000, step=1000) |
| Q5 | RAG on chunked index, compare token usage |
| Q6 | Agentic loop with `search` tool, count tool calls |

## Setup

### 1. Clone / navigate to the directory

```bash
cd cohorts/2026/01-agentic-rag
```

### 2. Install dependencies

Using `uv` (recommended):

```bash
uv add openai minsearch gitsource
```

Or with pip:

```bash
pip install openai minsearch gitsource
```

### 3. Set your API key

Copy the template and fill in your key:

```bash
cp .env.template .env
```

Or open `solution.py` and paste your key directly into the `OPENROUTER_API_KEY` variable:

```python
OPENROUTER_API_KEY = "sk-or-..."  # your key here
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys).

### 4. Run

```bash
python solution.py
```

The script runs all 6 questions end-to-end and prints a final summary.

## How It Works

### Data Fetching

`gitsource.GithubRepositoryDataReader` downloads every markdown file inside a `lessons/` folder from the course repo at commit `8c1834d`, ensuring reproducible results.

### Indexing (Q2)

`minsearch.Index` is built with:
- `text_fields=["content"]` — full-text search on lesson body
- `keyword_fields=["filename"]` — exact-match filter on file path

### RAG Pipeline (Q3)

1. Search index → top-5 results
2. Build context string from results
3. Send prompt + context to LLM
4. Return answer + token usage from `response.usage.prompt_tokens`

### Chunking (Q4–Q5)

`gitsource.chunk_documents(documents, size=2000, step=1000)` splits long pages into overlapping 2000-char windows (1000-char stride), giving better retrieval precision.

### Agentic Loop (Q6)

A manual OpenAI tool-calling loop:

```
User message
    └─► LLM (with search tool schema)
            ├─ tool_calls? → execute search() → append tool result → repeat
            └─ finish_reason=stop → return final answer
```

The agent is instructed to call `search` multiple times with different keywords before answering.

## Submit Results

https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw1
