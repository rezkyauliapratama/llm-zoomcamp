# LLM Zoomcamp — Homework

This folder contains all homework submissions for the [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) course.

## Structure

| Folder | Module | Topics |
|--------|--------|--------|
| `01-intro/` | Introduction | RAG basics, Elasticsearch, OpenAI API |
| `02-open-source/` | Open-Source LLMs | Ollama, HuggingFace, local inference |
| `03-vector-search/` | Vector Search | Embeddings, FAISS, hybrid search |
| `04-evaluation/` | Evaluation & Monitoring | ROUGE, LLM-as-judge, Grafana |
| `05-orchestration/` | Orchestration | Mage AI, pipeline automation |
| `06-best-practices/` | Best Practices | Prompt engineering, chunking, guardrails |
| `07-agentic-rag/` | Agentic RAG | ReAct, tool use, function calling |

## How to Run

Each homework folder contains:
- `README.md` — description and setup instructions
- `homework.ipynb` — solution notebook
- `requirements.txt` — Python dependencies

```bash
cd homework/<module-folder>
pip install -r requirements.txt
jupyter notebook homework.ipynb
```
