# Module 01 — Agentic RAG: Homework

> **Official homework:** [cohorts/2026/01-agentic-rag/homework.md](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md)

## Structure

```
module-01/
├── section-a-rag-fundamentals/   # Q1–Q5: RAG Pipeline
├── section-b-data-ingestion/     # Q6–Q7: SQLite/sqlitesearch
├── section-c-agents/             # Q8–Q12: Function Calling & Agentic Loop
├── bonus/                        # Bonus 1 & 2
├── data/                         # Local datasets / downloaded files
├── notebook.ipynb                # Main working notebook
└── README.md
```

## Question Summary

### Section A — RAG Fundamentals (Part 1)
| Q | Topic | Answer |
|---|-------|---------|
| Q1 | Dataset Exploration — total records for `data-engineering-zoomcamp` | TBD |
| Q2 | Search Basics — highest score for query `"How do I run Kafka?"` | TBD |
| Q3 | Prompt Construction — character length of built prompt | TBD |
| Q4 | RAG Pipeline E2E — most frequent word in LLM answer | TBD |
| Q5 | Token Usage — total `prompt_tokens` used | TBD |

### Section B — Data Ingestion
| Q | Topic | Answer |
|---|-------|---------|
| Q6 | SQLite Ingestion — time to index full dataset | TBD |
| Q7 | Persistence Validation — results identical after restart? | TBD |

### Section C — Agents & Function Calling (Part 2)
| Q | Topic | Answer |
|---|-------|---------|
| Q8 | Tool Definition — number of required parameters | TBD |
| Q9 | Function Calling Output — tool name and `query` argument | TBD |
| Q10 | Agentic Loop Iteration Count — iterations for multi-hop query | TBD |
| Q11 | No-Tool Scenario — did LLM call tools for "Thank you!"? | TBD |
| Q12 | Safety Limit — behavior with `max_iterations=3` | TBD |

### Bonus
| Q | Topic |
|---|-------|
| Bonus 1 | Multi-Source Agent — two tools across courses |
| Bonus 2 | Agent vs Fixed RAG comparison on 5 queries |

## Notes
- Dataset: DataTalksClub FAQ (`https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json`)
- Search engine: `minsearch` (Part 1), `sqlitesearch` (Part 2)
- LLM: OpenAI (or compatible)
- Framework: `ToyAIKit` for agentic loop
