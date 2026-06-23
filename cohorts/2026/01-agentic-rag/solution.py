#!/usr/bin/env python3
"""
Homework 01 - Agentic RAG
LLM Zoomcamp 2026

Model   : deepseek/deepseek-chat-v3-0324:free  (DeepSeek V3 via OpenRouter)
Search  : minsearch
Dataset : DataTalksClub/llm-zoomcamp lessons (commit 8c1834d)
"""

import json
from openai import OpenAI
from gitsource import GithubRepositoryDataReader, chunk_documents
import minsearch

# ---------------------------------------------------------------------------
# CONFIG - fill in your key directly here (or load from .env)
# ---------------------------------------------------------------------------
OPENROUTER_API_KEY = ""  # <-- paste your OpenRouter API key here
MODEL = "deepseek/deepseek-chat-v3-0324:free"   # DeepSeek V3 Flash via OpenRouter

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ---------------------------------------------------------------------------
# PREPARATION: pull lesson pages from GitHub
# ---------------------------------------------------------------------------
print("[1/6] Fetching lesson pages from GitHub (commit 8c1834d)...")
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

# ---------------------------------------------------------------------------
# Q1: How many lesson pages?
# ---------------------------------------------------------------------------
print(f"\n=== Q1: Number of lesson pages ===")
print(f"Total lesson pages: {len(documents)}")

# ---------------------------------------------------------------------------
# Q2: Indexing with minsearch and searching
# ---------------------------------------------------------------------------
print("\n[2/6] Building minsearch index...")
index = minsearch.Index(
    text_fields=["content"],
    keyword_fields=["filename"],
)
index.fit(documents)

Q2_QUERY = "How does the agentic loop keep calling the model until it stops?"
results = index.search(query=Q2_QUERY, num_results=5)

print(f"\n=== Q2: First search result ===")
print(f"Query : {Q2_QUERY}")
print(f"First result filename: {results[0]['filename']}")

# ---------------------------------------------------------------------------
# Q3: RAG - count input tokens
# ---------------------------------------------------------------------------
print("\n[3/6] Building RAG on the full-document index...")

def build_context(search_results: list[dict]) -> str:
    """Build context string from search results."""
    context_pieces = []
    for r in search_results:
        context_pieces.append(f"File: {r['filename']}\n\n{r['content']}")
    return "\n\n---\n\n".join(context_pieces)

def llm(prompt: str) -> tuple[str, object]:
    """Call the LLM and return (answer_text, usage)."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response.choices[0].message.content
    usage  = response.usage
    return answer, usage

def rag(query: str, idx: minsearch.Index, num_results: int = 5) -> tuple[str, object]:
    """Full RAG pipeline: search -> build context -> LLM."""
    results = idx.search(query=query, num_results=num_results)
    context = build_context(results)
    prompt = f"""You are a helpful course teaching assistant. 
Answer the question below based only on the context provided.

Context:
{context}

Question: {query}

Answer:"""
    answer, usage = llm(prompt)
    return answer, usage

answer_q3, usage_q3 = rag(Q2_QUERY, index)

print(f"\n=== Q3: Input tokens for RAG request ===")
print(f"Answer (truncated): {answer_q3[:200]}...")
print(f"Input (prompt) tokens: {usage_q3.prompt_tokens}")

# ---------------------------------------------------------------------------
# Q4: Chunking - how many chunks?
# ---------------------------------------------------------------------------
print("\n[4/6] Chunking documents (size=2000, step=1000)...")
chunks = chunk_documents(documents, size=2000, step=1000)

print(f"\n=== Q4: Number of chunks ===")
print(f"Total chunks: {len(chunks)}")

# ---------------------------------------------------------------------------
# Q5: RAG with chunked index - compare input tokens
# ---------------------------------------------------------------------------
print("\n[5/6] Building minsearch index on chunks...")
chunk_index = minsearch.Index(
    text_fields=["content"],
    keyword_fields=["filename"],
)
chunk_index.fit(chunks)

answer_q5, usage_q5 = rag(Q2_QUERY, chunk_index)

print(f"\n=== Q5: Input tokens comparison ===")
print(f"Full-doc index tokens : {usage_q3.prompt_tokens}")
print(f"Chunk index tokens    : {usage_q5.prompt_tokens}")
if usage_q3.prompt_tokens > 0:
    ratio = usage_q3.prompt_tokens / usage_q5.prompt_tokens
    print(f"Ratio (full / chunk)  : {ratio:.1f}x fewer with chunking")

# ---------------------------------------------------------------------------
# Q6: Agentic RAG with tool calling
# ---------------------------------------------------------------------------
print("\n[6/6] Running agentic RAG (tool-calling loop)...")

# Tool definition for the search function
SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search the course lesson knowledge base for relevant content.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up in the course lessons.",
                }
            },
            "required": ["query"],
        },
    },
}

def search(query: str) -> str:
    """Search the chunk index and return formatted results."""
    results = chunk_index.search(query=query, num_results=3)
    return build_context(results)

AGENT_INSTRUCTIONS = (
    "You're a course teaching assistant. Answer the student's question using the "
    "search tool. Make multiple searches with different keywords before answering."
)

Q6_QUERY = "How does the agentic loop work, and how is it different from plain RAG?"

messages = [
    {"role": "system", "content": AGENT_INSTRUCTIONS},
    {"role": "user",   "content": Q6_QUERY},
]

search_call_count = 0
max_iterations = 20

for iteration in range(max_iterations):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[SEARCH_TOOL],
        tool_choice="auto",
    )

    msg = response.choices[0].message
    finish_reason = response.choices[0].finish_reason

    # Append assistant message to history
    messages.append({"role": "assistant", "content": msg.content, "tool_calls": msg.tool_calls})

    if finish_reason == "stop" or not msg.tool_calls:
        # Agent decided to answer
        break

    # Process tool calls
    for tool_call in msg.tool_calls:
        if tool_call.function.name == "search":
            args = json.loads(tool_call.function.arguments)
            query_used = args["query"]
            search_call_count += 1
            print(f"  [Tool call #{search_call_count}] search('{query_used}')")
            result = search(query_used)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

final_answer = messages[-1]["content"] if messages[-1]["role"] == "assistant" else msg.content

print(f"\n=== Q6: Agent search call count ===")
print(f"Number of search() calls: {search_call_count}")
print(f"Final answer (truncated): {str(final_answer)[:300]}...")

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
print("\n" + "="*50)
print("HOMEWORK ANSWERS SUMMARY")
print("="*50)
print(f"Q1 - Lesson pages           : {len(documents)}")
print(f"Q2 - First result filename  : {results[0]['filename']}")
print(f"Q3 - Input tokens (full doc): {usage_q3.prompt_tokens}")
print(f"Q4 - Number of chunks       : {len(chunks)}")
print(f"Q5 - Input tokens (chunked) : {usage_q5.prompt_tokens}")
print(f"Q6 - Agent search calls     : {search_call_count}")
