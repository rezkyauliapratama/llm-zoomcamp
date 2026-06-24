"""
Homework 02 - Vector Search
LLM Zoomcamp 2026

Run:
    pip install -r requirements.txt
    python download.py
    python homework.py

Requires:
    - embedder.py (from course repo: 02-vector-search/embed/embedder.py)
    - download.py (from course repo: 02-vector-search/embed/download.py)
"""

import numpy as np
from pathlib import Path
from gitsource import GithubRepositoryDataReader, chunk_documents
from embedder import Embedder
from minsearch import VectorSearch, Index

# ── Setup ──────────────────────────────────────────────────────────────
EMBEDDER_PATH = "models/Xenova/all-MiniLM-L6-v2"
embedder = Embedder(EMBEDDER_PATH)

# ── Q1. Embedding a query ─────────────────────────────────────────────
query = "How does approximate nearest neighbor search work?"
v = embedder.encode(query)
print(f"Q1: v[0] = {v[0]:.4f}  → Closest option: -0.02")

# ── Loading the data ──────────────────────────────────────────────────
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [file.parse() for file in reader.read()]
doc_by_filename = {d["filename"]: d for d in documents}

# ── Q2. Cosine similarity ─────────────────────────────────────────────
target_file = "02-vector-search/lessons/07-sqlitesearch-vector.md"
target_doc = doc_by_filename[target_file]
doc_embedding = embedder.encode(target_doc["content"])
cos_sim = float(np.dot(v, doc_embedding))
print(f"Q2: Cosine similarity = {cos_sim:.4f}  → Closest option: 0.37")

# ── Q3. Chunking and search by hand ───────────────────────────────────
chunks = chunk_documents(documents, size=2000, step=1000)
chunk_texts = [c["content"] for c in chunks]
X = embedder.encode_batch(chunk_texts)
scores = X @ v
top_idx = int(np.argmax(scores))
top_chunk = chunks[top_idx]
print(f"Q3: Top chunk = {top_chunk['filename']}")

# ── Q4. Vector search with minsearch ──────────────────────────────────
vs = VectorSearch()
vs.fit(vectors=X, payload=chunks)

q4_query = "What metric do we use to evaluate a search engine?"
q4_v = embedder.encode(q4_query)
q4_results = vs.search(q4_v, num_results=5)
print(f"Q4: First result = {q4_results[0]['filename']}")

# ── Q5. Text search vs vector search ──────────────────────────────────
text_index = Index(text_fields=["content"], keyword_fields=[])
text_index.fit(chunks)

q5_query = "How do I store vectors in PostgreSQL?"
q5_v = embedder.encode(q5_query)
vector_results = vs.search(q5_v, num_results=5)
text_results = text_index.search(q5_query, num_results=5)

vec_filenames = {r["filename"] for r in vector_results}
txt_filenames = {r["filename"] for r in text_results}
in_vec_not_txt = list(vec_filenames - txt_filenames)
print(f"Q5: In vector but not text = {in_vec_not_txt}")

# ── Q6. Hybrid search ─────────────────────────────────────────────────
def rrf(result_lists, k=60, num_results=5):
    scores = {}
    docs = {}
    for results in result_lists:
        for rank, doc in enumerate(results):
            key = (doc["filename"], doc["start"])
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc
    ranked = sorted(scores, key=scores.get, reverse=True)
    return [docs[key] for key in ranked[:num_results]]

q6_query = "How do I give the model access to tools?"
q6_v = embedder.encode(q6_query)
vec_r = vs.search(q6_v, num_results=10)
txt_r = text_index.search(q6_query, num_results=10)
hybrid_r = rrf([vec_r, txt_r], k=60, num_results=5)
print(f"Q6: First after RRF = {hybrid_r[0]['filename']}")

print()
print("=== ALL ANSWERS ===")
print(f"Q1: {v[0]:.4f} → -0.02")
print(f"Q2: {cos_sim:.4f} → 0.37")
print(f"Q3: {top_chunk['filename']}")
print(f"Q4: {q4_results[0]['filename']}")
print(f"Q5: {in_vec_not_txt}")
print(f"Q6: {hybrid_r[0]['filename']}")
