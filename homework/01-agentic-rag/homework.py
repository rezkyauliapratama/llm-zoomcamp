"""
LLM Zoomcamp 2026 - Homework 01: Agentic RAG

Requirements:
    pip install gitsource toyaikit minsearch openai python-dotenv

Usage:
    1. Copy .env.template to .env and set OPENROUTER_API_KEY
       OR set API_KEY directly in this file (see below)
    2. Run: python homework.py
"""

import os
import json

# ==============================================================================
# API KEY CONFIGURATION
# Option 1: Set directly here (pure-python, no .env needed)
# Option 2: Load from .env via python-dotenv
# ==============================================================================
# API_KEY = "sk-or-v1-YOUR_KEY_HERE"   # <-- uncomment and set your key here

# If API_KEY is not set above, try loading from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# OpenRouter config
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324:free"  # deepseek-v3-flash on openrouter

# ==============================================================================
# STEP 1 — Load dataset from GitHub
# ==============================================================================

print("=" * 60)
print("Q1. Loading lesson pages from GitHub...")
print("=" * 60)

from gitsource import GithubRepositoryDataReader, chunk_documents

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

files = reader.read()

documents = []
for file in files:
    doc = file.parse()
    documents.append(doc)

print(f"Q1 Answer: Total lesson pages = {len(documents)}")

# ==============================================================================
# STEP 2 — Index with minsearch and search
# ==============================================================================

print("\n" + "=" * 60)
print("Q2. Indexing with minsearch...")
print("=" * 60)

from minsearch import Index

index = Index(
    text_fields=["content"],
    keyword_fields=["filename"],
)
index.fit(documents)

query_q2 = "How does the agentic loop keep calling the model until it stops?"
results_q2 = index.search(query=query_q2, num_results=5)

print(f"Q2 Answer: First result filename = {results_q2[0]['filename']}")
print(f"Top 3 results:")
for r in results_q2[:3]:
    print(f"  - {r['filename']}")

# ==============================================================================
# STEP 3 — RAG (full documents, no chunking)
# ==============================================================================

print("\n" + "=" * 60)
print("Q3. RAG with full documents...")
print("=" * 60)

from openai import OpenAI

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def build_context(search_results):
    context_parts = []
    for doc in search_results:
        context_parts.append(
            f"File: {doc['filename']}\n"
            f"Content:\n{doc['content']}\n"
        )
    return "\n---\n".join(context_parts)


def rag(query, search_index, num_results=5):
    results = search_index.search(query=query, num_results=num_results)
    context = build_context(results)

    prompt = f"""You are a helpful course teaching assistant.
Answer the question based on the context below.

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    return answer, input_tokens


answer_q3, tokens_q3 = rag(query_q2, index)
print(f"Q3 Answer (input tokens): {tokens_q3}")
print(f"RAG answer preview: {answer_q3[:200]}...")

# ==============================================================================
# STEP 4 — Chunking
# ==============================================================================

print("\n" + "=" * 60)
print("Q4. Chunking documents...")
print("=" * 60)

chunks = chunk_documents(documents, size=2000, step=1000)
print(f"Q4 Answer: Total chunks = {len(chunks)}")

# ==============================================================================
# STEP 5 — RAG with chunking
# ==============================================================================

print("\n" + "=" * 60)
print("Q5. RAG with chunked index...")
print("=" * 60)

chunk_index = Index(
    text_fields=["content"],
    keyword_fields=["filename"],
)
chunk_index.fit(chunks)

answer_q5, tokens_q5 = rag(query_q2, chunk_index)
print(f"Q5 Answer (input tokens with chunks): {tokens_q5}")
print(f"Reduction vs Q3: {tokens_q3} -> {tokens_q5} tokens")
if tokens_q5 > 0:
    ratio = tokens_q3 / tokens_q5
    print(f"Ratio: {ratio:.1f}x fewer tokens")

# ==============================================================================
# STEP 6 — Agentic RAG with toyaikit
# ==============================================================================

print("\n" + "=" * 60)
print("Q6. Agentic RAG with toyaikit...")
print("=" * 60)

try:
    from toyaikit import Agent, Tool

    search_call_count = 0

    def search(query: str) -> str:
        """
        Search the LLM Zoomcamp course lessons for information about a given topic.
        Returns relevant lesson content as a string.

        Args:
            query: The search query string to look up in the course materials
        """
        global search_call_count
        search_call_count += 1
        results = chunk_index.search(query=query, num_results=3)
        return build_context(results)

    agent = Agent(
        client=client,
        model=MODEL,
        system="""
You're a course teaching assistant. Answer the student's question using the
search tool. Make multiple searches with different keywords before answering.
""".strip(),
        tools=[Tool(search)],
    )

    agent_query = "How does the agentic loop work, and how is it different from plain RAG?"
    agent_answer = agent.run(agent_query)

    print(f"Q6 Answer: Agent called search {search_call_count} time(s)")
    print(f"Agent answer preview: {str(agent_answer)[:300]}...")

except ImportError:
    print("toyaikit not installed. Run: pip install toyaikit")
    print("Skipping Q6.")

# ==============================================================================
# SUMMARY
# ==============================================================================

print("\n" + "=" * 60)
print("HOMEWORK ANSWERS SUMMARY")
print("=" * 60)
print(f"Q1. Number of lesson pages     : {len(documents)}")
print(f"Q2. First result filename       : {results_q2[0]['filename']}")
print(f"Q3. Input tokens (no chunking)  : {tokens_q3}")
print(f"Q4. Number of chunks            : {len(chunks)}")
print(f"Q5. Input tokens (with chunks)  : {tokens_q5}")
try:
    print(f"Q6. Search tool calls by agent  : {search_call_count}")
except NameError:
    print("Q6. Skipped (toyaikit not installed)")
