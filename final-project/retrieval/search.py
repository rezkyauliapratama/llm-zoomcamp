"""Hybrid search: BM25 + dense vector retrieval."""

from typing import List, Dict


def vector_search(es_client, index_name: str, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    """Dense vector similarity search."""
    query = {
        "knn": {
            "field": "embedding",
            "query_vector": query_embedding,
            "k": top_k,
            "num_candidates": top_k * 10
        },
        "_source": ["doc_id", "title", "content", "source", "article"]
    }
    response = es_client.search(index=index_name, body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]


def hybrid_search(es_client, index_name: str, query_text: str, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    """Hybrid BM25 + vector search with RRF (Reciprocal Rank Fusion)."""
    query = {
        "retriever": {
            "rrf": {
                "retrievers": [
                    {
                        "standard": {
                            "query": {
                                "multi_match": {
                                    "query": query_text,
                                    "fields": ["title", "content"]
                                }
                            }
                        }
                    },
                    {
                        "knn": {
                            "field": "embedding",
                            "query_vector": query_embedding,
                            "k": top_k * 2
                        }
                    }
                ]
            }
        },
        "size": top_k
    }
    response = es_client.search(index=index_name, body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]
