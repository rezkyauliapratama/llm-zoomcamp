"""Cross-encoder reranker for OJK regulatory document retrieval.

Model: cross-encoder/ms-marco-MiniLM-L-6-v2
Alternative: Cohere Rerank API (set USE_COHERE=true in env)
"""

import os

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def rerank(query: str, documents: list[dict], top_k: int = 5) -> list[dict]:
    """Rerank documents using a cross-encoder model.

    Args:
        query: Original user query.
        documents: List of retrieved chunks with 'content' and metadata.
        top_k: Number of top-scored documents to return.

    Returns:
        Top-k documents sorted by reranker score (descending).
    """
    # TODO: Implement cross-encoder reranking
    # Option 1: sentence-transformers CrossEncoder
    # Option 2: Cohere Rerank API if USE_COHERE=true
    raise NotImplementedError("Reranker implementation pending")
