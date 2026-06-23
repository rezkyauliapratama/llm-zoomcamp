"""End-to-end RAG pipeline for OJK/BI Regulatory Intelligence Assistant."""

from generation.prompts import SYSTEM_PROMPT_V1, RAG_PROMPT_TEMPLATE, format_context
from retrieval.hybrid_search import hybrid_search
from retrieval.query_rewriter import rewrite_query
from retrieval.reranker import rerank


def rag(
    query: str,
    prompt_version: str = "v1",
    rewrite: bool = True,
    top_k: int = 5,
    llm_client=None,
) -> dict:
    """Full RAG pipeline: rewrite → retrieve → rerank → generate → log.

    Args:
        query: User's natural language question.
        prompt_version: 'v1' or 'v2' (for evaluation comparison).
        rewrite: Whether to rewrite query before retrieval.
        top_k: Number of chunks to pass to LLM.
        llm_client: LLM client instance.

    Returns:
        Dict with 'answer', 'sources', 'rewritten_query', 'chunks'.
    """
    # Step 1: Query Rewriting
    rewritten_query = rewrite_query(query, llm_client) if rewrite else query

    # Step 2: Hybrid Retrieval
    candidates = hybrid_search(rewritten_query, top_k=10)

    # Step 3: Reranking
    chunks = rerank(rewritten_query, candidates, top_k=top_k)

    # Step 4: Generation
    context = format_context(chunks)
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=query)
    system_prompt = SYSTEM_PROMPT_V1 if prompt_version == "v1" else SYSTEM_PROMPT_V1  # TODO: V2

    # TODO: Call LLM and return structured response
    raise NotImplementedError("RAG pipeline generation step pending")
