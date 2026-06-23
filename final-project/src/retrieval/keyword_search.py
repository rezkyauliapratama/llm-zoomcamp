"""Elasticsearch BM25 keyword search integration."""


def index_documents(docs: list[dict]) -> None:
    """Index documents into Elasticsearch."""
    # TODO: implement Elasticsearch indexing
    raise NotImplementedError


def search(query: str, top_k: int = 5) -> list[dict]:
    """BM25 keyword search in Elasticsearch."""
    # TODO: implement Elasticsearch search
    raise NotImplementedError
