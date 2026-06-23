"""LLM-as-a-Judge evaluation for generation quality."""

JUDGE_PROMPT = """
You are an expert evaluator for a regulatory RAG system.
Rate the following answer on a scale of 1-5 for each criterion:

1. **Relevance**: Does the answer directly address the question? (1=Not relevant, 5=Highly relevant)
2. **Faithfulness**: Is the answer grounded in the provided context without hallucination? (1=Hallucinated, 5=Fully grounded)
3. **Completeness**: Does the answer cover all key aspects of the question? (1=Incomplete, 5=Complete)

Question: {question}
Context: {context}
Answer: {answer}

Return JSON: {{"relevance": X, "faithfulness": X, "completeness": X, "reasoning": "..."}}
"""


def evaluate_answer(question: str, context: str, answer: str) -> dict:
    """Evaluate an answer using LLM-as-a-Judge."""
    # TODO: implement LLM judge call
    raise NotImplementedError
