# Module 01 - Agentic RAG: Homework

> **Source:** [DataTalksClub/llm-zoomcamp/cohorts/2026/01-agentic-rag/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)

## Overview

Homework untuk Module 01 mencakup dua bagian besar:
- **Section A & B** — RAG Fundamentals + Data Ingestion (Part 1)
- **Section C** — Agents & Function Calling (Part 2)

## Questions Summary

### Section A - RAG Fundamentals (Part 1)
| Q | Topic |
|---|-------|
| Q1 | Dataset Exploration — total records `data-engineering-zoomcamp` |
| Q2 | Search Basics — top score dari keyword search "How do I run Kafka?" |
| Q3 | Prompt Construction — panjang (chars) prompt dari top-3 results |
| Q4 | RAG Pipeline E2E — kata paling sering dari jawaban LLM |
| Q5 | Token Usage — total `prompt_tokens` pada Q4 |

### Section B - Data Ingestion
| Q | Topic |
|---|-------|
| Q6 | SQLite Ingestion — waktu (detik) index seluruh dataset |
| Q7 | Persistence Validation — validasi hasil search identik setelah restart |

### Section C - Agents & Function Calling (Part 2)
| Q | Topic |
|---|-------|
| Q8 | Tool Definition — jumlah required parameters |
| Q9 | Function Calling Output — tool name + query argument |
| Q10 | Agentic Loop Iteration Count |
| Q11 | No-Tool Scenario — apakah "Thank you!" trigger tool call? |
| Q12 | Safety Limit — behavior saat max_iterations=3 terlampaui |

### Bonus
- Bonus 1: Multi-Source Agent (2 tools: DE + ML Zoomcamp)
- Bonus 2: Agent vs Fixed RAG Comparison (5 queries)

## Files Structure

```
module-01-agentic-rag/
├── README.md               ← this file
├── notebook.ipynb          ← main homework notebook
├── minsearch.py            ← copy from course repo
├── rag.py                  ← RAG pipeline implementation
├── requirements.txt        ← pinned dependencies
└── answers.md              ← submitted answers
```

## Setup

```bash
cd homework/module-01-agentic-rag
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
jupyter notebook notebook.ipynb
```
