# Homework 01 — Agentic RAG

> LLM Zoomcamp 2026 · Module 1

## Overview

This homework builds a RAG system from scratch over the LLM Zoomcamp course lesson pages, then makes it **agentic** by giving the LLM a `search` tool.

| Component | Choice |
|-----------|--------|
| LLM Provider | [OpenRouter](https://openrouter.ai) |
| Model | `deepseek/deepseek-chat-v3-5` (DeepSeek V3 Flash) |
| Search | [`minsearch`](https://github.com/alexeygrigorev/minsearch) |
| Dataset | DataTalksClub/llm-zoomcamp lesson `.md` files · commit `8c1834d` |

---

## Questions

| # | Question | Approach |
|---|----------|----------|
| Q1 | How many lesson pages? | Count docs from `gitsource` reader |
| Q2 | Filename of first search result | Index with `minsearch`, search query |
| Q3 | Input tokens for RAG (full docs) | Modified `RAGBase.llm()` exposes `usage` |
| Q4 | How many chunks? | `chunk_documents(size=2000, step=1000)` |
| Q5 | Token reduction with chunking? | Compare Q3 vs Q4 prompt tokens |
| Q6 | How many times did agent call `search`? | OpenAI tool-calling agentic loop |

---

## Setup

### 1. Clone & enter directory

```bash
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/cohorts/2026/01-agentic-rag
```

### 2. Install dependencies

```bash
pip install openai minsearch gitsource
```

### 3. Set your API key

Copy `.env.template` to `.env` and fill in your key:

```bash
cp .env.template .env
```

Then open `.env` and set:

```
OPENROUTER_API_KEY=sk-or-...
```

**Or** set it directly inside `homework.py` at the `OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"` line.

### 4. Run

```bash
python homework.py
```

---

## File Structure

```
01-agentic-rag/
├── homework.py          # Main solution script (all 6 questions)
├── rag_helper.py        # Modified RAGBase for filename/content schema + usage reporting
├── .env.template        # API key template
└── README.md            # This file
```

---

## Key Modifications to `rag_helper.py`

The original `RAGBase` was written for the FAQ schema (`section`/`question`/`answer`). Two changes were made:

1. **`build_context`** — adapted to `filename` + `content` fields from `gitsource`.
2. **`llm` + `rag`** — now return the full response object so `usage.prompt_tokens` is accessible for Q3 and Q5.

The LLM client is switched from the OpenAI Responses API to **OpenAI Chat Completions** (`chat.completions.create`) to stay compatible with OpenRouter.

---

## Notes

- If your answers differ slightly from the official options, pick the closest one — token counts vary by model/provider.
- The agentic loop (Q6) uses a native OpenAI tool-calling loop instead of `toyaikit`; the result is equivalent.
- DeepSeek V3 Flash is extremely cost-efficient on OpenRouter (~$0.14/M input tokens as of 2026).

---

## Submit

https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw1
