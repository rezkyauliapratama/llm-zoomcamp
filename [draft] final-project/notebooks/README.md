# Notebooks

Exploratory Jupyter notebooks untuk development dan experimentation.

## Notebooks

```
notebooks/
├── README.md
├── 01_data_exploration.ipynb       ← explore OJK document structure
├── 02_chunking_experiments.ipynb   ← test chunking strategies
├── 03_embedding_experiments.ipynb  ← test embedding models
├── 04_retrieval_experiments.ipynb  ← test retrieval approaches
├── 05_llm_prompts.ipynb            ← test prompt versions
└── 06_evaluation_report.ipynb      ← final evaluation results
```

## Setup

```bash
cd final-project
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
jupyter notebook
```
