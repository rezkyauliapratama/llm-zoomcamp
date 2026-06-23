# Evaluation

Offline evaluation of both retrieval quality and LLM generation quality.

## Evaluation Plan

### Retrieval Evaluation
Compare 4 retrieval approaches to earn full score (2/2):

| Approach | Expected Hit Rate@5 | Expected MRR | Decision |
|----------|--------------------|--------------|---------|
| Keyword-only (FTS/BM25) | Baseline | Baseline | Reject |
| Vector-only (dense) | +10-15% | +10% | Compare |
| Hybrid RRF | Best | Best | **Use this** |
| Hybrid + reranker | Marginal improvement | Marginal | Bonus |

### LLM Evaluation
Evaluate 2 prompt versions:
- **V1**: Strict citation-only
- **V2**: Structured numbered response with per-point citations

LLM-as-a-Judge dimensions:
1. **Relevance** — does it answer the question?
2. **Faithfulness** — grounded in context (no hallucination)?
3. **Citation accuracy** — are pasal references correct?

## Ground Truth

Synthetic Q&A pairs generated from regulatory chunks:
- Target: ~150–200 Q&A pairs
- Stored as `data/eval_questions.csv`
- Columns: `question, expected_answer, source_document, pasal`
