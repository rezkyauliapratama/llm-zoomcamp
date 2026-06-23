"""Index documents into Elasticsearch vector store."""

from typing import List, Dict


def create_index(es_client, index_name: str, dims: int = 1536) -> None:
    """Create Elasticsearch index with dense vector mapping."""
    mapping = {
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword"},
                "title": {"type": "text"},
                "content": {"type": "text"},
                "source": {"type": "keyword"},
                "article": {"type": "keyword"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }
    es_client.indices.create(index=index_name, body=mapping, ignore=400)


def index_documents(es_client, index_name: str, documents: List[Dict]) -> None:
    """Bulk index documents with embeddings."""
    from elasticsearch.helpers import bulk
    actions = [
        {
            "_index": index_name,
            "_id": doc["doc_id"],
            "_source": doc
        }
        for doc in documents
    ]
    bulk(es_client, actions)
    print(f"Indexed {len(documents)} documents into '{index_name}'")
