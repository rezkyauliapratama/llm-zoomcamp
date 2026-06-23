"""Retrieval evaluation: Hit Rate@K and MRR across multiple retrieval approaches.

Approaches evaluated:
    1. Keyword-only (PostgreSQL FTS)
    2. Vector-only (PGVector dense)
    3. Hybrid RRF (vector + keyword)
    4. Hybrid RRF + reranker (bonus)
"""

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class RetrievalMetrics:
    approach: str
    hit_rate_at_5: float
    mrr: float
    avg_latency_ms: float


def hit_rate_at_k(results: list[dict], relevant_pasal: str, k: int = 5) -> bool:
    """Check if the relevant pasal appears in the top-k retrieved chunks."""
    for chunk in results[:k]:
        if chunk.get("pasal") == relevant_pasal:
            return True
    return False


def mean_reciprocal_rank(results: list[dict], relevant_pasal: str) -> float:
    """Calculate MRR for a single query."""
    for rank, chunk in enumerate(results, 1):
        if chunk.get("pasal") == relevant_pasal:
            return 1.0 / rank
    return 0.0


def evaluate_retrieval(
    eval_questions_path: Path,
    search_fn,
    approach_name: str,
    k: int = 5,
) -> RetrievalMetrics:
    """Run full retrieval evaluation on a ground truth dataset.

    Args:
        eval_questions_path: Path to CSV with question, expected_answer, source_document, pasal.
        search_fn: Callable(query) → list of chunk dicts.
        approach_name: Human-readable name for this approach.
        k: Top-K cutoff for Hit Rate.

    Returns:
        RetrievalMetrics with hit_rate_at_k, mrr, avg_latency.
    """
    # TODO: Implement evaluation loop
    raise NotImplementedError("Retrieval evaluation pending")
