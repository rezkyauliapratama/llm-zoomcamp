# Homework 01 — Agentic RAG

> **LLM Zoomcamp 2026 · Module 1**  
> Course: [DataTalksClub/llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)  
> Homework spec: [cohorts/2026/01-agentic-rag/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)

---

## Overview

Build a RAG system over the LLM Zoomcamp course lesson pages, then make it agentic. This covers:

| # | Topic |
|---|-------|
| Q1 | Count lesson pages loaded from GitHub |
| Q2 | Index with `minsearch` and search |
| Q3 | RAG pipeline (measure input tokens) |
| Q4 | Chunk documents with `gitsource` |
| Q5 | RAG with chunked index (compare token counts) |
| Q6 | Agentic RAG with `toyaikit` (count tool calls) |

---

## Stack

| Component | Choice |
|-----------|--------|
| LLM Provider | [OpenRouter](https://openrouter.ai) |
| Model | `deepseek/deepseek-chat-v3-0324:free` |
| Search | `minsearch` (simple in-memory full-text) |
| Data loader | `gitsource` |
| Agent framework | `toyaikit` |

---

## Setup

### 1. Clone and navigate

```bash
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/homework/01-agentic-rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API key

**Option A — via `.env`** (recommended):
```bash
cp .env.template .env
# Edit .env and set OPENROUTER_API_KEY=sk-or-v1-...
```

**Option B — directly in the script**:
Open `homework.py` and uncomment this line near the top:
```python
# API_KEY = "sk-or-v1-YOUR_KEY_HERE"
```

Get your API key at [openrouter.ai/keys](https://openrouter.ai/keys).

---

## Run

```bash
python homework.py
```

The script runs all 6 questions sequentially and prints a summary at the end.

---

## Dataset

Lesson pages are fetched directly from the course repository at commit `8c1834d`:

```
DataTalksClub/llm-zoomcamp @ 8c1834d
└── {01..07}-*/lessons/*.md
```

Modules covered:
- `01-agentic-rag`
- `02-vector-search`
- `03-orchestration`
- `04-evaluation`
- `05-monitoring`
- `06-best-practices`
- `07-project-example`

---

## File Structure

```
homework/01-agentic-rag/
├── homework.py        # Main script — runs all Q1–Q6
├── minsearch.py       # Minimal in-memory search engine
├── requirements.txt   # Python dependencies
├── .env.template      # API key template (copy to .env)
└── README.md          # This file
```

---

## Notes

- Token counts in Q3 and Q5 may vary slightly depending on the model/provider. Select the closest answer option.
- For Q6, the number of `search` tool calls depends on the model's behaviour — it varies between runs. Select the closest option.
- `minsearch.py` is bundled locally for zero-dependency simplicity (no pip install needed for it).
