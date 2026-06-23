"""Retrieval evaluation metrics: Hit Rate, MRR, NDCG."""


def hit_rate(relevant_docs: list[str], retrieved_docs: list[str], k: int = 5) -> float:
    """Calculate Hit Rate @k — fraction of queries where at least one relevant doc is retrieved."""
    # TODO: implement
    raise NotImplementedError


def mrr(relevant_docs: list[str], retrieved_docs: list[str], k: int = 5) -> float:
    """Calculate Mean Reciprocal Rank @k."""
    # TODO: implement
    raise NotImplementedError
