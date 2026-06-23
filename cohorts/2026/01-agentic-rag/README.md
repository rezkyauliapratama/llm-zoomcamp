# Homework 01 — Agentic RAG

> LLM Zoomcamp 2026 · Module 01

This homework builds a RAG system from scratch using the **course lesson pages** as the knowledge base, then turns it into an agentic system where the LLM decides when and what to search.

---

## Stack

| Component | Choice |
|-----------|--------|
| **LLM** | `deepseek/deepseek-chat-v3-0324` via [OpenRouter](https://openrouter.ai) |
| **Search** | [`minsearch`](https://github.com/alexeygrigorev/minsearch) — simple in-memory full-text search |
| **Dataset** | DataTalksClub/llm-zoomcamp lesson pages @ commit `8c1834d` |
| **Data loader** | [`gitsource`](https://github.com/alexeygrigorev/gitsource) |

---

## Setup

### 1. Clone & navigate

```bash
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/cohorts/2026/01-agentic-rag
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenRouter API key

Open `homework.py` and paste your key into the `OPENROUTER_API_KEY` variable at the top:

```python
OPENROUTER_API_KEY = "sk-or-..."
```

> A `.env.template` is also provided if you prefer environment-variable management later.

---

## Run

```bash
python homework.py
```

The script runs all six questions sequentially and prints the answers.

---

## Questions overview

| # | Topic | Key detail |
|---|-------|------------|
| Q1 | Dataset size | Count lesson pages loaded via `gitsource` |
| Q2 | Indexing & search | First result filename for the agentic-loop query |
| Q3 | RAG | Input token count when using full document context |
| Q4 | Chunking | Number of chunks with `size=2000, step=1000` |
| Q5 | RAG + chunking | Token reduction vs. full-document RAG |
| Q6 | Agentic loop | Number of `search` tool calls by the LLM agent |

---

## How the agentic loop works (Q6)

The agent is given a `search` function as a tool. The LLM decides autonomously:

1. Call `search` with a query → get lesson context
2. Decide whether it has enough information
3. If not → call `search` again with different keywords
4. Once satisfied → return the final answer (no more tool calls)

This mirrors the agentic pattern from the module: the LLM drives the loop, unlike plain RAG where search runs exactly once with the raw user query.

---

## Submit results

https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw1
