# Homework 1 - Agentic RAG

LLM Zoomcamp 2026 · Module 01 · Agentic RAG

## Overview

Build a RAG system from scratch over the LLM Zoomcamp course lessons themselves,
then turn it into an agentic system that decides on its own when and what to search.

**Dataset** : `DataTalksClub/llm-zoomcamp` @ commit `8c1834d` — all `lessons/*.md` files  
**Model** : `openai/gpt-4.1-mini` via [OpenRouter](https://openrouter.ai) (equivalent to `gpt-5.4-mini`)  
**Search** : `minsearch` — local in-memory full-text search, no server needed

---

## File Structure

```
homework/01-agentic-rag/
├── .env.template       # copy to .env and fill in OPENROUTER_API_KEY
├── homework.py         # main script - runs Q1 through Q6 end-to-end
├── rag_helper.py       # RAGBase class (adapted from DataTalksClub original)
├── minsearch.py        # lightweight in-memory full-text search index
├── requirements.txt    # pip-compatible dependency list
└── README.md           # this file
```

---

## Setup

### 1. Clone and enter the directory

```bash
git clone https://github.com/rezkyauliapratama/llm-zoomcamp.git
cd llm-zoomcamp/homework/01-agentic-rag
```

### 2. Install dependencies

With `uv` (recommended):

```bash
uv add openai python-dotenv gitsource
```

Or with `pip`:

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.template .env
```

Edit `.env` and set your key:

```env
OPENROUTER_API_KEY=sk-or-...
```

Get a free API key at [openrouter.ai/keys](https://openrouter.ai/keys).

### 4. Run

```bash
python homework.py
```

---

## Code Structure

### `rag_helper.py` - RAGBase

Adapted from the [DataTalksClub original](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-agentic-rag/code/rag_helper.py).
Key differences from the original:

| Method | Original (FAQ schema) | This version (lessons schema) |
|---|---|---|
| `search()` | Uses `boost_dict` + `filter_dict` for FAQ fields | Plain search - no boost or filter |
| `build_context()` | Formats `section` / `Q:` / `A:` | Formats `## filename` + `content` |
| `llm()` | `responses.create(input=...)` - OpenAI only | `chat.completions.create(messages=...)` - OpenRouter compatible; returns full response |
| `rag()` | Returns `str` | Returns `RAGResult(answer, input_tokens, output_tokens)` |

Usage:

```python
from rag_helper import RAGBase

rag = RAGBase(index=my_index, llm_client=client, model="openai/gpt-4.1-mini")
result = rag.rag("How does the agentic loop work?")

print(result.answer)
print(result.input_tokens)
print(result.output_tokens)
```

### `homework.py` - Main Script

Runs all six homework questions in sequence:

| Step | Question | What it does |
|---|---|---|
| 1 | Q1 | Loads lesson pages from GitHub via `gitsource` - counts total documents |
| 2 | Q2 | Indexes documents with `minsearch` - runs first search, returns top filename |
| 3 | Q3 | Full-document RAG via `RAGBase` - measures input token count |
| 4 | Q4 | Chunks documents with `chunk_documents(size=2000, step=1000)` - counts chunks |
| 5 | Q5 | Chunked RAG via `RAGBase` - compares token count vs Q3 |
| 6 | Q6 | Agentic RAG - hand-written `while True` loop with `chat.completions` + tool calling |

#### Q6 - Agentic Loop Design

Instead of a third-party agent framework (which requires OpenAI's Responses API),
Q6 uses a hand-written agentic loop - the same pattern that `toyaikit` uses internally:

```python
while True:
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto"
    )
    msg = response.choices[0].message
    messages.append(msg)

    if not msg.tool_calls:   # model is done
        break

    for tc in msg.tool_calls:
        result = search(**json.loads(tc.function.arguments))
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
```

This approach is 100% compatible with OpenRouter and any `chat.completions`-compatible provider.

---

## Expected Output

```
[1] Loading lesson pages from GitHub...
Q1 - Number of lesson pages: 72

[2] Indexing documents with minsearch...
Q2 - Filename of first result: 01-agentic-rag/lessons/14-agentic-loop.md

[3] Running RAG over full-document index...
Q3 - Input tokens (full-doc RAG): ~7000

[4] Chunking documents...
Q4 - Number of chunks: 295

[5] Indexing chunks and running chunked RAG...
Q5 - Input tokens (chunked RAG): ~700
     Ratio full/chunked: ~3x fewer tokens with chunking

[6] Building agentic RAG (hand-written loop)...
Q6 - Number of search() calls: 4

- All questions answered!
```

> Token counts are approximate and depend on the model/provider used.
> If your answers do not match exactly, select the closest option.

---

## Why OpenRouter instead of OpenAI directly?

OpenRouter provides a unified API over many model providers using the standard
`openai.OpenAI` client - just set a different `base_url` and `api_key`:

```python
from openai import OpenAI

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)
```

Model names follow the `provider/model-name` convention (e.g. `openai/gpt-4.1-mini`,
`deepseek/deepseek-v4-flash`). Browse available models at [openrouter.ai/models](https://openrouter.ai/models).

---

## References

- [Homework instructions](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)
- [DataTalksClub LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)
- [gitsource](https://github.com/alexeygrigorev/gitsource)
- [minsearch](https://github.com/alexeygrigorev/minsearch)
- [OpenRouter](https://openrouter.ai)
