"""LLM-based query rewriter for Indonesian regulatory queries.

Expands abbreviations and adds regulatory context keywords before retrieval.

Examples:
    "batas npl" → "batas rasio Non-Performing Loan NPL perbankan regulasi OJK Bank Indonesia"
    "kewajiban ai" → "kewajiban bank penerapan kecerdasan artifisial AI tata kelola OJK panduan 2025"
"""

QUERY_REWRITER_PROMPT = """Rewrite the user's question into a precise search query for a database
of Indonesian banking regulations (OJK and Bank Indonesia).

Rules:
- Expand abbreviations (POJK, SE, GWM, NPL, LCR, CAR, BMPK, etc.)
- Add regulatory context keywords if missing
- Include both Bahasa Indonesia and English terms for technical concepts
- If already precise, return unchanged
- Output ONLY the rewritten query, no explanation

Original query: {query}
Rewritten query:"""


def rewrite_query(query: str, llm_client=None) -> str:
    """Rewrite a user query to improve regulatory document retrieval.

    Args:
        query: Raw user query.
        llm_client: LLM client (OpenAI-compatible).

    Returns:
        Rewritten query string optimized for regulatory document search.
    """
    # TODO: Implement LLM query rewriting
    # Call LLM with QUERY_REWRITER_PROMPT, return cleaned output
    raise NotImplementedError("Query rewriter implementation pending")
