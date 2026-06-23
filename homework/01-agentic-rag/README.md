# 📝 Homework 01 — Agentic RAG

> **Module:** 01 - Agentic RAG  
> **Official Homework:** [cohorts/2026/01-agentic-rag/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)  

---

## 🗂 Structure

```
01-agentic-rag/
├── README.md              # This file
├── notebook.ipynb         # Main solution notebook
├── requirements.txt       # Python dependencies
├── rag_base.py            # RAGBase class (Part 1)
├── agentic_rag.py         # AgenticRAG class (Part 2)
├── data/
│   └── documents.db       # SQLite index (auto-generated)
└── answers.md             # Final answers to submit
```

---

## 📋 Questions

### Section A — RAG Fundamentals (Part 1)

| # | Question | Status |
|---|----------|--------|
| Q1 | Dataset Exploration — total records for `data-engineering-zoomcamp` | ⬜ |
| Q2 | Search Basics — highest score for `"How do I run Kafka?"` | ⬜ |
| Q3 | Prompt Construction — character length of built prompt | ⬜ |
| Q4 | RAG Pipeline End-to-End — most frequent word in LLM answer | ⬜ |
| Q5 | Token Usage — total `prompt_tokens` used in Q4 | ⬜ |

### Section B — Data Ingestion

| # | Question | Status |
|---|----------|--------|
| Q6 | SQLite Ingestion — indexing time in seconds | ⬜ |
| Q7 | Persistence Validation — identical results after restart? | ⬜ |

### Section C — Agents & Function Calling (Part 2)

| # | Question | Status |
|---|----------|--------|
| Q8 | Tool Definition — number of required parameters | ⬜ |
| Q9 | Function Calling Output — tool name and `query` argument value | ⬜ |
| Q10 | Agentic Loop Iteration Count — iterations for complex query | ⬜ |
| Q11 | No-Tool Scenario — does `"Thank you!"` trigger tool call? | ⬜ |
| Q12 | Safety Limit — behavior with `max_iterations=3` | ⬜ |

### Bonus

| # | Question | Status |
|---|----------|--------|
| B1 | Multi-Source Agent — does agent call both tools? | ⬜ |
| B2 | Agent vs Fixed RAG Comparison — 5 query comparison | ⬜ |

---

## 🚀 Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY=your_key_here

# Launch notebook
jupyter notebook notebook.ipynb
```

---

## 📦 Dependencies

See [`requirements.txt`](./requirements.txt).
