#!/usr/bin/env python3
"""
Homework 1 - Agentic RAG
LLM Zoomcamp 2026 - Cohort 01-agentic-rag

Dataset : DataTalksClub/llm-zoomcamp @ commit 8c1834d (lessons/*.md)
Model   : openai/gpt-4.1-mini via OpenRouter
Search  : minsearch (local, no server needed)
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index
from rag_helper import RAGBase

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Add it to .env file.")

MODEL = "openai/gpt-4.1-mini"  # gpt-5.4-mini equivalent via OpenRouter
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

# ---------------------------------------------------------------------------
# Step 1 - Load documents from GitHub (pinned commit)
# ---------------------------------------------------------------------------
print("[1] Loading lesson pages from GitHub...")
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
    
print(f"Q1 - Number of lesson pages: {len(documents)}")

# ---------------------------------------------------------------------------
# Step 2 - Index with minsearch (full documents) and run first search
# ---------------------------------------------------------------------------
print("\n[2] Indexing documents with minsearch...")
doc_index = Index(text_fields=["content"], keyword_fields=["filename"])
doc_index.fit(documents)

Q2_QUERY = "How does the agentic loop keep calling the model until it stops?"
results = doc_index.search(Q2_QUERY, num_results=5)
print(f"Q2 - Filename of first result: {results[0]['filename']}")

# ---------------------------------------------------------------------------
# Step 3 - RAG over full-document index
# ---------------------------------------------------------------------------
print("\n[3] Running RAG over full-document index...")

rag_full = RAGBase(index=doc_index, llm_client=client, model=MODEL)
q3_result = rag_full.rag(Q2_QUERY)

print(f"Q3 - Input tokens (full-doc RAG): {q3_result.input_tokens}")
print(f"     Answer preview: {q3_result.answer[:200]}...")

# ---------------------------------------------------------------------------
# Step 4 - Chunking
# ---------------------------------------------------------------------------
print("\n[4] Chunking documents...")
chunks = chunk_documents(documents, size=2000, step=1000)
print(f"Q4 - Number of chunks: {len(chunks)}")

# ---------------------------------------------------------------------------
# Step 5 - RAG over chunk index
# ---------------------------------------------------------------------------
print("\n[5] Indexing chunks and running chunked RAG...")
chunk_index = Index(text_fields=["content"], keyword_fields=["filename"])
chunk_index.fit(chunks)

rag_chunked = RAGBase(index=chunk_index, llm_client=client, model=MODEL)
q5_result = rag_chunked.rag(Q2_QUERY)

print(f"Q5 - Input tokens (chunked RAG): {q5_result.input_tokens}")
ratio = q3_result.input_tokens / max(q5_result.input_tokens, 1)
print(f"     Ratio full/chunked: {ratio:.1f}x fewer tokens with chunking")

# ---------------------------------------------------------------------------
# Step 6 - Agentic RAG (hand-written loop, OpenRouter-compatible)
# ---------------------------------------------------------------------------
print("\n[6] Building agentic RAG (hand-written loop)...")

search_call_count = 0


def search(query: str) -> str:
    """Search the LLM Zoomcamp course lessons for information.
    Use specific keywords related to the topic you want to learn about.
    """
    global search_call_count
    search_call_count += 1
    results = rag_chunked.search(query, num_results=3)
    return rag_chunked.build_context(results)


# Tool schema - derived from search() signature + docstring
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "Search the LLM Zoomcamp course lessons for information. "
                "Use specific keywords related to the topic you want to learn about."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                    }
                },
                "required": ["query"],
            },
        },
    }
]

SYSTEM_PROMPT = (
    "You're a course teaching assistant. "
    "Answer the student's question using the search tool. "
    "Make multiple searches with different keywords before answering."
)

Q6_QUERY = "How does the agentic loop work, and how is it different from plain RAG?"

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": Q6_QUERY},
]

# Agentic loop - same while True pattern as toyaikit internally uses
while True:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    msg = response.choices[0].message
    messages.append(msg)

    # No tool calls - model is done, final answer ready
    if not msg.tool_calls:
        break

    # Execute every tool call the model requested
    for tc in msg.tool_calls:
        args = json.loads(tc.function.arguments)
        result = search(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": result,
        })

final_answer = messages[-1].content if hasattr(messages[-1], "content") else messages[-1]["content"]
print(f"Q6 - Number of search() calls: {search_call_count}")
print(f"     Answer preview: {final_answer[:200]}...")

print("\n- All questions answered!")
