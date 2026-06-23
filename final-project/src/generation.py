"""
LLM Generation Module

Builds prompts from retrieved context and generates cited answers
using OpenAI GPT-4o or a local open-source model via Ollama.
"""

from typing import List, Dict, Optional


RAG_PROMPT_TEMPLATE = """
You are a regulatory compliance expert for Indonesian financial institutions.
Answer the question below ONLY based on the provided context from OJK/BI regulations.
Always cite the specific regulation name and article number.

Context:
{context}

Question: {question}

Answer (with citations):
"""


def build_context(retrieved_docs: List[Dict], max_tokens: int = 2000) -> str:
    """Format retrieved documents into a context string for the prompt."""
    # TODO: implement context builder with token budget
    raise NotImplementedError


def generate_answer(
    question: str,
    retrieved_docs: List[Dict],
    model: str = "gpt-4o",
    temperature: float = 0.0,
) -> Dict:
    """
    Generate a grounded, cited answer from retrieved regulatory context.

    Returns:
        dict with keys: answer, sources, model, prompt_tokens, completion_tokens
    """
    # TODO: implement LLM generation
    raise NotImplementedError
