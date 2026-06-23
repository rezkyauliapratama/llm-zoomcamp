"""Reciprocal Rank Fusion (RRF) implementation for hybrid search."""
from typing import List, Dict, Any


def rrf_fusion(
    ranked_lists: List[List[Dict[str, Any]]],
    id_key: str = "id",
    k: int = 60,
) -> List[Dict[str, Any]]:
    """
    Combine multiple ranked lists using Reciprocal Rank Fusion.

    Args:
        ranked_lists: List of ranked document lists. Each list is a list of
                      dicts with at least the `id_key` field.
        id_key: Field name to use as document identifier.
        k: RRF smoothing constant (default=60).

    Returns:
        Merged list of documents sorted by descending RRF score.

    Formula:
        RRF_score(d) = Σ 1 / (k + rank(d))  for all ranked_lists
    """
    scores: Dict[str, float] = {}
    doc_map: Dict[str, Dict[str, Any]] = {}

    for ranked_list in ranked_lists:
        for rank, doc in enumerate(ranked_list, start=1):
            doc_id = doc[id_key]
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
            if doc_id not in doc_map:
                doc_map[doc_id] = doc

    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [
        {**doc_map[doc_id], "rrf_score": scores[doc_id]}
        for doc_id in sorted_ids
    ]


if __name__ == "__main__":
    # Quick test
    list1 = [{"id": "doc1"}, {"id": "doc2"}, {"id": "doc3"}]
    list2 = [{"id": "doc2"}, {"id": "doc1"}, {"id": "doc4"}]
    result = rrf_fusion([list1, list2])
    for doc in result:
        print(f"{doc['id']}: {doc['rrf_score']:.4f}")
