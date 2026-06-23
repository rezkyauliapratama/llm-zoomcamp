#!/usr/bin/env python3
"""
Homework 1 - Agentic RAG
LLM Zoomcamp 2026 - Cohort 01-agentic-rag

Dataset : DataTalksClub/llm-zoomcamp @ commit 8c1834d (lessons/*.md)
Model   : deepseek/deepseek-chat-v4-flash via OpenRouter
Search  : minsearch (local, no server needed)
"""

import os
from dataclasses import dataclass
from openai import OpenAI
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# TODO: put your key here, or set the OPENROUTER_API_KEY environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

MODEL = "deepseek/deepseek-chat-v4-flash"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

# ---------------------------------------------------------------------------
# Step 1 – Load documents from GitHub (pinned commit)
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
documents = [f.parse() for f in files]

print(f"Q1 – Number of lesson pages: {len(documents)}")

# ---------------------------------------------------------------------------
# Step 2 – Index with minsearch (full documents) and run first search
# ---------------------------------------------------------------------------
print("\n[2] Indexing documents with minsearch...")
doc_index = Index(text_fields=["content"], keyword_fields=["filename"])
doc_index.fit(documents)

Q2_QUERY = "How does the agentic loop keep calling the model until it stops?"
results = doc_index.search(Q2_QUERY, num_results=5)
print(f"Q2 – Filename of first result: {results[0]['filename']}")

# ---------------------------------------------------------------------------
# Step 3 – RAG over full-document index
# ---------------------------------------------------------------------------
print("\n[3] Building RAG over full-document index...")


def build_context(results, max_chars=8000):
    ctx = ""
    for r in results:
        ctx += f"## {r['filename']}\n{r['content']}\n\n"
        if len(ctx) >= max_chars:
            break
    return ctx.strip()


@dataclass
class RAGResult:
    answer: str
    input_tokens: int
    output_tokens: int


def rag(query: str, index: Index, num_results: int = 5) -> RAGResult:
    search_results = index.search(query, num_results=num_results)
    context = build_context(search_results)
    prompt = (
        "You are a helpful course assistant.\n\n"
        "Use the context below to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful course assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    answer = response.choices[0].message.content
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    return RAGResult(answer=answer, input_tokens=input_tokens, output_tokens=output_tokens)


q3_result = rag(Q2_QUERY, doc_index)
print(f"Q3 – Input tokens (full-doc RAG): {q3_result.input_tokens}")
print(f"     Answer preview: {q3_result.answer[:200]}...")

# ---------------------------------------------------------------------------
# Step 4 – Chunking
# ---------------------------------------------------------------------------
print("\n[4] Chunking documents...")
chunks = chunk_documents(documents, size=2000, step=1000)
print(f"Q4 – Number of chunks: {len(chunks)}")

# ---------------------------------------------------------------------------
# Step 5 – RAG over chunk index
# ---------------------------------------------------------------------------
print("\n[5] Indexing chunks and running chunked RAG...")
chunk_index = Index(text_fields=["content"], keyword_fields=["filename"])
chunk_index.fit(chunks)

q5_result = rag(Q2_QUERY, chunk_index)
print(f"Q5 – Input tokens (chunked RAG): {q5_result.input_tokens}")
ratio = q3_result.input_tokens / max(q5_result.input_tokens, 1)
print(f"     Ratio full/chunked: {ratio:.1f}x fewer tokens with chunking")

# ---------------------------------------------------------------------------
# Step 6 – Agentic RAG with toyaikit
# ---------------------------------------------------------------------------
print("\n[6] Building agentic RAG with toyaikit...")
try:
    from toyaikit import Agent, tool

    search_call_count = 0

    @tool
    def search(query: str) -> str:
        """Search the LLM Zoomcamp course lessons for information.
        Use specific keywords related to the topic you want to learn about.
        """
        global search_call_count
        search_call_count += 1
        results = chunk_index.search(query, num_results=3)
        return build_context(results, max_chars=3000)

    agent = Agent(
        client=client,
        model=MODEL,
        tools=[search],
        system_prompt=(
            "You're a course teaching assistant. "
            "Answer the student's question using the search tool. "
            "Make multiple searches with different keywords before answering."
        ),
    )

    Q6_QUERY = "How does the agentic loop work, and how is it different from plain RAG?"
    answer = agent.run(Q6_QUERY)
    print(f"Q6 – Number of search() calls: {search_call_count}")
    print(f"     Answer preview: {answer[:200]}...")

except ImportError:
    print("toyaikit not installed. Run: pip install toyaikit")
    print("Skipping Q6.")

print("\n✅ All questions answered!")
