"""Qdrant vector store integration."""


def index_documents(docs: list[dict]) -> None:
    """Index documents with their embeddings into Qdrant."""
    # TODO: implement Qdrant client indexing
    raise NotImplementedError


def search(query_vector: list[float], top_k: int = 5) -> list[dict]:
    """Search Qdrant for top-k most similar documents."""
    # TODO: implement Qdrant similarity search
    raise NotImplementedError
