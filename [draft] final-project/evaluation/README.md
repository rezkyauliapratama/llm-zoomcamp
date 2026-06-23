# Evaluation

Retrieval dan LLM evaluation untuk OJK/BI RAG system.

## Overview

Evaluasi mencakup dua dimensi:
1. **Retrieval Evaluation** — seberapa baik sistem menemukan chunk yang relevan
2. **LLM Evaluation** — seberapa baik LLM menghasilkan jawaban dari chunk yang ditemukan

## Files

```
evaluation/
├── README.md
├── generate_ground_truth.py     ← LLM-generated synthetic Q&A pairs
├── evaluate_retrieval.py        ← Hit Rate@k + MRR metrics
├── evaluate_llm.py              ← LLM-as-a-Judge evaluation
├── compare_approaches.py        ← Compare keyword vs vector vs hybrid
├── notebooks/
│   ├── 01_ground_truth_gen.ipynb
│   ├── 02_retrieval_eval.ipynb
│   └── 03_llm_eval.ipynb
└── data/
    ├── ground_truth.csv         ← synthetic Q&A dataset (gitignored if large)
    └── eval_results/            ← evaluation run results
```

## Ground Truth Generation

Synthetic Q&A pairs dibuat dari regulatory chunks:
- Input: each regulatory pasal text
- Output: 2–3 questions per pasal
- Target: ~150–200 Q&A pairs
- Format: `question, expected_answer, source_document, pasal`

## Retrieval Metrics

| Metric | Formula |
|--------|---------|
| **Hit Rate@k** | Proportion of questions where correct pasal is in top-k results |
| **MRR** | `1/N × Σ 1/rank(first_correct)` |

## Retrieval Approaches Compared

| Approach | Expected Result |
|----------|-----------------|
| Keyword-only (BM25/FTS) | Baseline |
| Vector-only (dense) | +10-15% over baseline |
| Hybrid RRF | Best overall |
| Hybrid + Reranker | Marginal improvement + bonus point |

## LLM Evaluation (LLM-as-a-Judge)

Two prompt versions evaluated:
- **Prompt V1**: Strict citation-only
- **Prompt V2**: Structured response with numbered points

Judge evaluates on 3 dimensions:
1. **Relevance** — does it answer the question?
2. **Faithfulness** — grounded in context (no hallucination)?
3. **Citation accuracy** — are pasal references correct?
