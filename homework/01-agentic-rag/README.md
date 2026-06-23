# Homework 1 — Agentic RAG

> **LLM Zoomcamp 2026 · Module 01**
> Reference: [homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)

---

## Overview

Builds a RAG system over the LLM Zoomcamp course lessons, then evolves it into an agentic pipeline where the LLM decides when and what to search.

**Stack:**
- 🔍 **Search:** `minsearch` (TF-IDF, local, no server needed)
- 🤖 **LLM:** `deepseek/deepseek-chat-v3-0324:free` via [OpenRouter](https://openrouter.ai)
- 📦 **Data loader:** `gitsource` (commit `8c1834d` — fixed for reproducibility)
- 🛠 **Agent:** hand-written tool-calling loop (OpenAI-compatible API)

---

## Questions Covered

| Q | Topic | Key Concept |
|---|-------|-------------|
| Q1 | Dataset size | How many lesson pages exist in the course repo |
| Q2 | Indexing & search | `minsearch` with `content` (text) + `filename` (keyword) |
| Q3 | RAG | Full-page RAG, measure input tokens |
| Q4 | Chunking | `size=2000, step=1000` sliding window |
| Q5 | RAG + chunking | Compare input tokens vs Q3 |
| Q6 | Agentic RAG | Function-calling loop, count `search` tool invocations |

---

## Setup

### 1. Clone & navigate

```bash
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/homework/01-agentic-rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your OpenRouter API key

Copy the template and fill in your key:

```bash
cp .env.template .env
# edit .env and set OPENROUTER_API_KEY=sk-or-...
```

Or export it directly:

```bash
export OPENROUTER_API_KEY="sk-or-your-key-here"
```

> Get a free key at [openrouter.ai/keys](https://openrouter.ai/keys).
> `deepseek/deepseek-chat-v3-0324:free` has a free tier — no credit card needed.

### 4. Run

```bash
python homework.py
```

---

## File Structure

```
homework/01-agentic-rag/
├── homework.py        # Main script — all 6 questions
├── minsearch.py       # Local TF-IDF search engine
├── requirements.txt   # Python dependencies
├── .env.template      # API key template
└── README.md          # This file
```

---

## How It Works

### Data Loading (Q1)
`gitsource.GithubRepositoryDataReader` pulls all `*.md` files under `/lessons/` at commit `8c1834d`. This pins the dataset so everyone gets the same answers.

### Search (Q2)
`minsearch.Index` builds an in-memory TF-IDF index. `content` is a text field (tokenized + scored), `filename` is a keyword field (exact match filter). No external services required.

### RAG (Q3)
Top-5 search results → concatenated context → prompt → LLM. Input token count is read from `response.usage.prompt_tokens`.

### Chunking (Q4–Q5)
`gitsource.chunk_documents(documents, size=2000, step=1000)` splits long pages into overlapping 2000-char windows with 1000-char steps. Each chunk retains `filename`. Chunked RAG sends fewer tokens per request.

### Agentic Loop (Q6)
A minimal tool-calling loop built on the OpenAI-compatible API:
1. System prompt instructs the model to search multiple times before answering
2. Model returns `tool_calls` → we execute `search()` → append result to messages
3. Loop continues until the model returns a final text answer (no tool calls)
4. We count total `search` invocations

---

## Notes

- Token counts (Q3, Q5) may differ slightly from `gpt-5.4-mini` reference answers because DeepSeek uses a different tokenizer. Select the closest option when submitting.
- The number of agent search calls (Q6) is non-deterministic — the model decides autonomously.
- The `minsearch.py` bundled here is a self-contained copy for portability.

---

## Submit

https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw1
