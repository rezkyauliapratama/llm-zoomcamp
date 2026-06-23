"""Hybrid search combining vector (Qdrant) and keyword (Elasticsearch) results."""


def hybrid_search(query: str, query_vector: list[float], top_k: int = 5, alpha: float = 0.5) -> list[dict]:
    """Combine BM25 and vector search using Reciprocal Rank Fusion (RRF).
    
    Args:
        query: Raw text query for BM25 search.
        query_vector: Embedding vector for semantic search.
        top_k: Number of results to return.
        alpha: Weight balance between semantic (alpha) and keyword (1-alpha).
    """
    # TODO: implement RRF or linear combination
    raise NotImplementedError
