"""Reranking retrieved documents for improved relevance."""

from typing import List, Dict


def rerank_with_cross_encoder(query: str, documents: List[Dict], top_k: int = 3) -> List[Dict]:
    """Rerank documents using a cross-encoder model."""
    from sentence_transformers import CrossEncoder
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    pairs = [(query, doc["content"]) for doc in documents]
    scores = model.predict(pairs)
    ranked = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:top_k]]


def rerank_with_llm(query: str, documents: List[Dict], llm_client, top_k: int = 3) -> List[Dict]:
    """LLM-based reranking: ask LLM to score relevance."""
    scored = []
    for doc in documents:
        prompt = f"""Rate the relevance of this document to the query on a scale of 1-10.
Query: {query}
Document: {doc['content'][:500]}
Respond with only a number."""
        response = llm_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5
        )
        score = float(response.choices[0].message.content.strip())
        scored.append((score, doc))
    ranked = sorted(scored, key=lambda x: x[0], reverse=True)
    return [doc for _, doc in ranked[:top_k]]
