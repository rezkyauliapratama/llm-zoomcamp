"""Text embedding generation for regulatory documents."""

from typing import List
import numpy as np


def get_embeddings_openai(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Generate embeddings using OpenAI API."""
    from openai import OpenAI
    client = OpenAI()
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]


def get_embeddings_local(texts: List[str], model_name: str = "BAAI/bge-m3") -> np.ndarray:
    """Generate embeddings using a local HuggingFace model."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return model.encode(texts, normalize_embeddings=True)
