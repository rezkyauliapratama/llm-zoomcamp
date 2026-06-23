"""LLM-as-a-Judge evaluation for generated answers.

Dimensions:
    - Relevance: does the answer address the question?
    - Faithfulness: is the answer grounded in context (no hallucination)?
    - Citation accuracy: are pasal references correct?

Prompt versions evaluated:
    - V1: Strict citation-only
    - V2: Structured response with numbered points
"""

JUDGE_PROMPT = """You are evaluating an AI assistant that answers questions about Indonesian banking regulations.

Question: {question}
Retrieved Context: {context}
Generated Answer: {answer}

Evaluate the answer on three dimensions. Respond with JSON:
{{
    "relevance": "good" | "neutral" | "bad",
    "faithfulness": "good" | "neutral" | "bad",
    "citation_accuracy": "good" | "neutral" | "bad",
    "overall": "good" | "neutral" | "bad",
    "explanation": "..."
}}"""


def judge_answer(question: str, context: str, answer: str, llm_client=None) -> dict:
    """Evaluate a single answer using LLM-as-a-Judge.

    Returns:
        Dict with relevance, faithfulness, citation_accuracy, overall, explanation.
    """
    # TODO: Implement LLM judge call
    raise NotImplementedError("LLM judge implementation pending")
