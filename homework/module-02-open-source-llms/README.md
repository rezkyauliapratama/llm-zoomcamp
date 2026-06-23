# Module 02 - Open-Source LLMs: Homework

> **Source:** [DataTalksClub/llm-zoomcamp/cohorts/2026/02-open-source/](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026)

## Overview

Modul ini membahas cara menjalankan LLM open-source secara lokal menggunakan Ollama dan Hugging Face models.

**Key Topics:**
- Ollama setup dan model management
- Hugging Face inference API
- Local inference vs cloud API trade-offs
- Running models: Llama, Mistral, Phi, Gemma

## Files Structure

```
module-02-open-source-llms/
├── README.md               ← this file
├── notebook.ipynb          ← main homework notebook
├── requirements.txt        ← pinned dependencies
└── answers.md              ← submitted answers
```

## Setup

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.2

cd homework/module-02-open-source-llms
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```
