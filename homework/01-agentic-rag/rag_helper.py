#!/usr/bin/env python3
"""
rag_helper.py - Reusable RAG utilities for homework/01-agentic-rag

Provides:
- build_context()  : format minsearch results into a prompt context string
- RAGResult        : dataclass to hold answer + token usage
- rag()            : single-turn RAG using minsearch Index + OpenAI-compatible client
"""

from dataclasses import dataclass
from minsearch import Index


def build_context(results: list[dict], max_chars: int = 8000) -> str:
    """Concatenate search results into a context block, capped at max_chars."""
    ctx = ""
    for r in results:
        ctx += f"## {r['filename']}\n{r['content']}\n\n"
        if len(ctx) >= max_chars:
            break
    return ctx.strip()


@dataclass
class RAGResult:
    """Container for a RAG response with token usage metadata."""
    answer: str
    input_tokens: int
    output_tokens: int


def rag(
    query: str,
    index: Index,
    client,
    model: str,
    num_results: int = 5,
    max_context_chars: int = 8000,
) -> RAGResult:
    """
    Run a single-turn RAG pipeline.

    Args:
        query            : User question.
        index            : Fitted minsearch.Index instance.
        client           : OpenAI-compatible client (e.g. openai.OpenAI).
        model            : Model identifier string.
        num_results      : Number of documents to retrieve.
        max_context_chars: Max characters to include in the context block.

    Returns:
        RAGResult with answer text and token counts.
    """
    search_results = index.search(query, num_results=num_results)
    context = build_context(search_results, max_chars=max_context_chars)

    prompt = (
        "You are a helpful course assistant.\n\n"
        "Use the context below to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful course assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return RAGResult(
        answer=response.choices[0].message.content,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
    )
