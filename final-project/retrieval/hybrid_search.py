"""Hybrid search: RRF fusion of PGVector (dense) + PostgreSQL FTS (sparse).

RRF Formula:
    RRF_score(d) = Σ 1 / (k + rank(d))  across all ranked lists
    where k=60 (standard smoothing constant)
"""

from typing import Any

RRF_K = 60


def reciprocal_rank_fusion(ranked_lists: list[list[dict]], k: int = RRF_K) -> list[dict]:
    """Fuse multiple ranked result lists using Reciprocal Rank Fusion.

    Args:
        ranked_lists: List of ranked document lists. Each list contains dicts
                      with at least 'id' and optional metadata.
        k: Smoothing constant (default: 60).

    Returns:
        Single merged list sorted by descending RRF score.
    """
    # TODO: Implement RRF fusion
    # 1. For each document across all lists, compute sum of 1/(k+rank)
    # 2. Merge metadata from original results
    # 3. Return sorted by RRF score descending
    raise NotImplementedError("RRF fusion implementation pending")


def vector_search(query: str, top_k: int = 10, filters: dict | None = None) -> list[dict]:
    """Dense vector search via PGVector."""
    # TODO: Implement PGVector cosine similarity search
    # Use multilingual-e5-base with 'query:' prefix for query encoding
    raise NotImplementedError("Vector search implementation pending")


def keyword_search(query: str, top_k: int = 10, filters: dict | None = None) -> list[dict]:
    """Sparse keyword search via PostgreSQL FTS (tsvector)."""
    # TODO: Implement PostgreSQL FTS search
    # Use plainto_tsquery or websearch_to_tsquery for query parsing
    raise NotImplementedError("Keyword search implementation pending")


def hybrid_search(query: str, top_k: int = 5, filters: dict | None = None) -> list[dict]:
    """Full hybrid search: vector + keyword → RRF fusion.

    Args:
        query: User query string (already rewritten if applicable).
        top_k: Number of final results to return after RRF.
        filters: Optional metadata filters (document_type, tahun_terbit, etc.)

    Returns:
        Top-k chunks sorted by RRF score.
    """
    vector_results = vector_search(query, top_k=10, filters=filters)
    keyword_results = keyword_search(query, top_k=10, filters=filters)
    fused = reciprocal_rank_fusion([vector_results, keyword_results])
    return fused[:top_k]
