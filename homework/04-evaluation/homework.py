"""
Homework 04 - Evaluation
LLM Zoomcamp 2026

Run:
    uv sync
    uv run python homework.py

Requires:
    - ground-truth.csv (download from course repo)
    - .env with OPENAI_API_KEY
"""

import os
import json
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import OpenAI
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index
from sentence_transformers import SentenceTransformer

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------------------------------
# Setup: Load documents and create chunks
# ---------------------------------------------------------------------------
print("Loading course documents...")
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [file.parse() for file in reader.read()]
print(f"Loaded {len(documents)} documents")

print("Creating chunks...")
chunks = chunk_documents(documents, size=2000, step=1000)
print(f"Created {len(chunks)} chunks")

# ---------------------------------------------------------------------------
# Load ground truth
# ---------------------------------------------------------------------------
gt_path = "ground-truth.csv"
if not os.path.exists(gt_path):
    print("Downloading ground-truth.csv...")
    import requests
    url = "https://raw.githubusercontent.com/DataTalksClub/llm-zoomcamp/main/cohorts/2026/04-evaluation/ground-truth.csv"
    r = requests.get(url)
    with open(gt_path, "wb") as f:
        f.write(r.content)

gt_df = pd.read_csv(gt_path)
ground_truth = gt_df.to_dict(orient="records")
print(f"Loaded {len(ground_truth)} ground truth questions")

# ---------------------------------------------------------------------------
# Q1: Average input tokens
# ---------------------------------------------------------------------------
print("\n=== Q1: Average input tokens ===")

class Questions(BaseModel):
    questions: list[str] = Field(description="List of 5 questions")

Q1_PAGES = [
    "01-agentic-rag/lessons/01-intro.md",
    "01-agentic-rag/lessons/02-environment.md",
    "01-agentic-rag/lessons/03-rag.md",
]

data_gen_instructions = """
You emulate a student who is taking our LLM course.
You are given one lesson page from the course.
Formulate 5 questions this student might ask that are answered by this page.

Rules:
- The page should contain the answer to each question.
- Make the questions complete and not too short.
- Use as few words as possible from the page; don't copy its phrasing.
- The questions should resemble how people actually ask things online:
  not too formal, not too short, not too long.
- Ask about the content of the lesson, not about its formatting or filename.
""".strip()

doc_by_filename = {d["filename"]: d for d in documents}
input_tokens_list = []

for page_file in Q1_PAGES:
    doc = doc_by_filename[page_file]
    user_prompt = json.dumps({"filename": doc["filename"], "content": doc["content"]})
    messages = [
        {"role": "developer", "content": data_gen_instructions},
        {"role": "user", "content": user_prompt},
    ]
    response = client.responses.parse(
        model="gpt-5.4-mini",
        input=messages,
        text_format=Questions,
    )
    input_tokens_list.append(response.usage.input_tokens)

avg_input = sum(input_tokens_list) / len(input_tokens_list)
print(f"Input tokens per page: {input_tokens_list}")
print(f"Average input tokens: {avg_input:.0f}")
print(f"Closest option: ~1400")

# ---------------------------------------------------------------------------
# Build search indices
# ---------------------------------------------------------------------------
print("\nBuilding search indices...")

# Text (keyword) index
text_index = Index(text_fields=["content"], keyword_fields=["filename"])
text_index.fit(chunks)

def text_search(query, num_results=5):
    return text_index.search(query, num_results=num_results)

# Vector search with sentence-transformers
print("Loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_texts = [c["content"] for c in chunks]
chunk_vectors = model.encode(chunk_texts, show_progress_bar=True)
print(f"Computed embeddings: {chunk_vectors.shape}")

def vector_search(query, num_results=5):
    q_vec = model.encode([query])[0]
    scores = chunk_vectors @ q_vec
    top_indices = np.argsort(scores)[::-1][:num_results]
    return [chunks[i] for i in top_indices]

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

def hybrid_search(query, k=60, num_results=5):
    text_results = text_search(query, num_results=10)
    vector_results = vector_search(query, num_results=10)
    return rrf([text_results, vector_results], k=k, num_results=num_results)

# ---------------------------------------------------------------------------
# Q2: First result with text search
# ---------------------------------------------------------------------------
print("\n=== Q2: First result with text search ===")

q = ground_truth[0]["question"]
text_results = text_search(q, num_results=5)
text_first = text_results[0]["filename"]
print(f"Question: {q[:80]}...")
print(f"First text result: {text_first}")

# ---------------------------------------------------------------------------
# Q3: First result with vector search
# ---------------------------------------------------------------------------
print("\n=== Q3: First result with vector search ===")

vector_results = vector_search(q, num_results=5)
vec_first = vector_results[0]["filename"]
print(f"First vector result: {vec_first}")
print(f"Note: question generated from 01-agentic-rag/lessons/01-intro.md")

# ---------------------------------------------------------------------------
# Evaluation functions
# ---------------------------------------------------------------------------
print("\nEvaluating all 360 questions...")

def compute_relevance(search_fn, q, correct_fn, num_results=5):
    results = search_fn(q, num_results=num_results)
    return [1 if r["filename"] == correct_fn else 0 for r in results]

def hit_rate(relevance_list):
    return np.mean([any(r) for r in relevance_list])

def mrr(relevance_list):
    total = 0.0
    for rel in relevance_list:
        for rank, r in enumerate(rel):
            if r == 1:
                total += 1.0 / (rank + 1)
                break
    return total / len(relevance_list)

def evaluate(search_fn, ground_truth, num_results=5):
    rel_list = []
    for item in ground_truth:
        rel = compute_relevance(search_fn, item["question"], item["filename"], num_results)
        rel_list.append(rel)
    return {"hit_rate": hit_rate(rel_list), "mrr": mrr(rel_list)}

# ---------------------------------------------------------------------------
# Q4: Evaluating text search
# ---------------------------------------------------------------------------
print("\n=== Q4: Evaluating text search ===")
text_metrics = evaluate(text_search, ground_truth)
print(f"Text search Hit Rate: {text_metrics['hit_rate']:.3f}")
print(f"Text search MRR:      {text_metrics['mrr']:.3f}")

# ---------------------------------------------------------------------------
# Q5: Evaluating vector search
# ---------------------------------------------------------------------------
print("\n=== Q5: Evaluating vector search ===")
vec_metrics = evaluate(vector_search, ground_truth)
print(f"Vector search Hit Rate: {vec_metrics['hit_rate']:.3f}")
print(f"Vector search MRR:      {vec_metrics['mrr']:.3f}")

# ---------------------------------------------------------------------------
# Q6: Tuning hybrid search
# ---------------------------------------------------------------------------
print("\n=== Q6: Tuning hybrid search RRF k ===")

k_values = [1, 50, 100, 200]
results = {}
for k in k_values:
    def make_hybrid(k_val):
        return lambda q, num_results=5: hybrid_search(q, k=k_val, num_results=num_results)
    metrics = evaluate(make_hybrid(k), ground_truth)
    results[k] = metrics
    print(f"  k={k:>3}: Hit Rate={metrics['hit_rate']:.3f}, MRR={metrics['mrr']:.3f}")

best_k = max(results, key=lambda k: results[k]["mrr"])
print(f"\nBest k for RRF: {best_k}")

# ---------------------------------------------------------------------------
# All answers
# ---------------------------------------------------------------------------
print("\n" + "=" * 50)
print("ALL ANSWERS")
print("=" * 50)
print(f"Q1: ~{avg_input:.0f}  → closest option: 1400")
print(f"Q2: {text_first}")
print(f"Q3: {vec_first}")
print(f"Q4: Hit Rate = {text_metrics['hit_rate']:.2f}")
print(f"Q5: MRR = {vec_metrics['mrr']:.2f}")
print(f"Q6: best k = {best_k}")
