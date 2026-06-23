#!/usr/bin/env python3
"""
Homework 01: Agentic RAG
LLM Zoomcamp 2026

Model  : deepseek/deepseek-chat-v3-5  (OpenRouter)
Search : minsearch
Dataset: DataTalksClub/llm-zoomcamp lesson markdown files (commit 8c1834d)

Usage:
    Set OPENROUTER_API_KEY below or in .env, then run:
        python homework.py
"""

import minsearch
from openai import OpenAI
from gitsource import GithubRepositoryDataReader, chunk_documents
from rag_helper import RAGBase

# ─────────────────────────────────────────────
# CONFIG — put your key here or use .env
# ─────────────────────────────────────────────
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"   # ← replace or export as env var

MODEL = "deepseek/deepseek-chat-v3-5"            # OpenRouter model id for DeepSeek V3 (Flash)
QUERY = "How does the agentic loop keep calling the model until it stops?"
AGENT_QUERY = "How does the agentic loop work, and how is it different from plain RAG?"

# ─────────────────────────────────────────────
# OpenRouter client (OpenAI-compatible)
# ─────────────────────────────────────────────
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


# ─────────────────────────────────────────────
# PREPARATION — download lesson pages
# ─────────────────────────────────────────────
print("Downloading lesson pages from GitHub (commit 8c1834d)...")
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

files = reader.read()
documents = [file.parse() for file in files]

# ─────────────────────────────────────────────
# Q1 — How many lesson pages?
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("Q1. How many lesson pages?")
print(f"   Answer: {len(documents)}")


# ─────────────────────────────────────────────
# Q2 — Index documents and search
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("Q2. Indexing with minsearch and searching...")

index = minsearch.Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)
index.fit(documents)

results = index.search(QUERY, num_results=5)
print(f"   Top result filename: {results[0]['filename']}")


# ─────────────────────────────────────────────
# Q3 — RAG (full documents)
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("Q3. RAG with full documents...")

rag = RAGBase(
    index=index,
    llm_client=client,
    model=MODEL
)

answer_q3, usage_q3 = rag.rag(QUERY)
print(f"   Answer: {answer_q3[:200]}...")
print(f"   Input tokens: {usage_q3.prompt_tokens}")


# ─────────────────────────────────────────────
# Q4 — Chunking
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("Q4. Chunking documents (size=2000, step=1000)...")

chunks = chunk_documents(documents, size=2000, step=1000)
print(f"   Number of chunks: {len(chunks)}")


# ─────────────────────────────────────────────
# Q5 — RAG with chunked index
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("Q5. RAG with chunked documents...")

chunk_index = minsearch.Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)
chunk_index.fit(chunks)

chunk_rag = RAGBase(
    index=chunk_index,
    llm_client=client,
    model=MODEL
)

answer_q5, usage_q5 = chunk_rag.rag(QUERY)
print(f"   Answer: {answer_q5[:200]}...")
print(f"   Input tokens (chunked): {usage_q5.prompt_tokens}")
print(f"   Input tokens (full):    {usage_q3.prompt_tokens}")
if usage_q3.prompt_tokens > 0:
    ratio = usage_q3.prompt_tokens / max(usage_q5.prompt_tokens, 1)
    print(f"   Reduction ratio: ~{ratio:.1f}x fewer tokens")


# ─────────────────────────────────────────────
# Q6 — Agentic RAG with search tool
# ─────────────────────────────────────────────
print("\n" + "="*50)
print("Q6. Agentic RAG with search tool...")

import json

AGENT_INSTRUCTIONS = (
    "You're a course teaching assistant. Answer the student's question using the "
    "search tool. Make multiple searches with different keywords before answering."
)

# Tool schema for search
tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the course knowledge base for relevant lesson content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def search_tool(query: str) -> str:
    """Search the chunk index and return formatted results."""
    results = chunk_index.search(query, num_results=5)
    lines = []
    for doc in results:
        lines.append(f"File: {doc['filename']}")
        lines.append(doc['content'])
        lines.append("")
    return "\n".join(lines).strip()


# Agentic loop
messages = [
    {"role": "system", "content": AGENT_INSTRUCTIONS},
    {"role": "user", "content": AGENT_QUERY}
]

search_call_count = 0
max_iterations = 20  # safety cap

for iteration in range(max_iterations):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message
    messages.append(msg)

    # Check if the model wants to call tools
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            if tool_call.function.name == "search":
                search_call_count += 1
                args = json.loads(tool_call.function.arguments)
                print(f"   [Tool call #{search_call_count}] search('{args['query'][:60]}...')")
                result = search_tool(args["query"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
    else:
        # No more tool calls — agent finished
        print(f"   Agent finished after {search_call_count} search call(s).")
        print(f"   Final answer: {msg.content[:300]}...")
        break

print(f"\n   Q6 Answer: search() called {search_call_count} time(s).")

print("\n" + "="*50)
print("Homework complete!")
