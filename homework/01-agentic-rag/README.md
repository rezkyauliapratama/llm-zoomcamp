# Homework 1 – Agentic RAG

> **LLM Zoomcamp 2026 · Module 01-agentic-rag**

Official homework spec → [cohorts/2026/01-agentic-rag/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)

---

## Overview

Build a RAG system over the LLM Zoomcamp lesson pages, then progressively improve it:

| Step | What we do |
|------|------------|
| Q1 | Count lesson pages fetched from GitHub |
| Q2 | Index with **minsearch** and do a first search |
| Q3 | Full RAG pipeline, measure input tokens |
| Q4 | Chunk documents (size=2000, step=1000) and count chunks |
| Q5 | RAG over chunk index, compare token usage |
| Q6 | **Agentic RAG** — give an LLM a `search` tool via toyaikit |

---

## Tech Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| LLM | `deepseek/deepseek-chat-v4-flash` via **OpenRouter** | Fast, cheap, OpenAI-compatible API |
| Search | **minsearch** (local, pure-Python) | Simple BM25-style, zero infra |
| Data loader | **gitsource** | Downloads pinned commit from GitHub |
| Agent framework | **toyaikit** | Lightweight tool-calling loop from the course |

---

## Setup

### 1. Clone & navigate

```bash
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/homework/01-agentic-rag
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenRouter API key

Option A – environment variable (recommended):
```bash
cp .env.template .env
# Edit .env and paste your key
export OPENROUTER_API_KEY=sk-or-...
```

Option B – edit `homework.py` directly:
```python
OPENROUTER_API_KEY = "sk-or-your-key-here"
```

Get a free key at <https://openrouter.ai/keys>.

---

## Run

```bash
python homework.py
```

Expected output (values are approximate):

```
[1] Loading lesson pages from GitHub...
Q1 – Number of lesson pages: 72

[2] Indexing documents with minsearch...
Q2 – Filename of first result: 01-agentic-rag/lessons/14-agentic-loop.md

[3] Building RAG over full-document index...
Q3 – Input tokens (full-doc RAG): ~7000

[4] Chunking documents...
Q4 – Number of chunks: 295

[5] Indexing chunks and running chunked RAG...
Q5 – Input tokens (chunked RAG): ~700
     Ratio full/chunked: ~10x fewer tokens with chunking

[6] Building agentic RAG with toyaikit...
Q6 – Number of search() calls: 4
```

---

## Project Structure

```
homework/01-agentic-rag/
├── .env.template      # API key template (copy to .env)
├── homework.py        # Main solution script (all 6 questions)
├── minsearch.py       # Local minsearch implementation
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## Notes

- The dataset is pinned to commit `8c1834d` of the DataTalksClub/llm-zoomcamp repo so results are reproducible.
- Token counts for Q3/Q5 may vary slightly depending on model and API version.
- Q6 agent call count may vary (LLM decides autonomously); closest option is **4**.
- Submit answers at <https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw1>.
