#!/usr/bin/env python3
"""
Homework 1 - Agentic RAG
LLM Zoomcamp 2026 - Module 01

Ref: https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2026/01-agentic-rag/homework.md

Model: deepseek/deepseek-chat-v3-0324:free via OpenRouter
"""

import json
import os
from openai import OpenAI
from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index

# ============================================================
# CONFIG - provide your OpenRouter API key here or via .env
# ============================================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODEL = "deepseek/deepseek-chat-v3-0324:free"


# ============================================================
# STEP 1: LOAD DATASET
# ============================================================
def load_documents():
    print("Loading lesson pages from GitHub (commit 8c1834d)...")
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )
    files = reader.read()
    documents = [file.parse() for file in files]
    print(f"Q1 - Number of lesson pages: {len(documents)}")
    return documents


# ============================================================
# STEP 2: INDEX & SEARCH (Q2)
# ============================================================
def build_index(documents):
    index = Index(text_fields=["content"], keyword_fields=["filename"])
    index.fit(documents)
    return index


def q2_search(index):
    query = "How does the agentic loop keep calling the model until it stops?"
    results = index.search(query, num_results=5)
    print(f"Q2 - First result filename: {results[0]['filename']}")
    return results


# ============================================================
# STEP 3: RAG (Q3)
# ============================================================
def build_context(results):
    context_parts = []
    for doc in results:
        context_parts.append(f"Filename: {doc['filename']}\n\n{doc['content']}")
    return "\n\n---\n\n".join(context_parts)


def llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response


def rag(query, index, num_results=5):
    results = index.search(query, num_results=num_results)
    context = build_context(results)
    prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {query}

Answer:"""
    response = llm(prompt)
    answer = response.choices[0].message.content
    usage = response.usage
    return answer, usage


def q3_rag(index):
    query = "How does the agentic loop keep calling the model until it stops?"
    answer, usage = rag(query, index)
    print(f"Q3 - RAG Answer:\n{answer}")
    print(f"Q3 - Input (prompt) tokens: {usage.prompt_tokens}")
    return usage.prompt_tokens


# ============================================================
# STEP 4: CHUNKING (Q4)
# ============================================================
def q4_chunking(documents):
    chunks = chunk_documents(documents, size=2000, step=1000)
    print(f"Q4 - Number of chunks: {len(chunks)}")
    return chunks


# ============================================================
# STEP 5: RAG WITH CHUNKING (Q5)
# ============================================================
def q5_rag_with_chunks(chunks, q3_tokens):
    chunk_index = build_index(chunks)
    query = "How does the agentic loop keep calling the model until it stops?"
    answer, usage = rag(query, chunk_index)
    print(f"Q5 - RAG with chunks answer:\n{answer}")
    print(f"Q5 - Input tokens (chunked): {usage.prompt_tokens}")
    ratio = q3_tokens / usage.prompt_tokens if usage.prompt_tokens else 0
    print(f"Q5 - Token ratio (full vs chunked): {ratio:.1f}x fewer with chunks")
    return chunk_index


# ============================================================
# STEP 6: AGENTIC RAG (Q6)
# ============================================================
def q6_agent(chunk_index):
    search_calls = [0]  # mutable counter

    def search(query: str) -> str:
        """
        Search the LLM Zoomcamp course lessons.
        Use this to look up information about RAG, agents, evaluation, monitoring, and best practices.

        Args:
            query: The search query string

        Returns:
            Relevant lesson content as a string
        """
        search_calls[0] += 1
        results = chunk_index.search(query, num_results=3)
        parts = [f"[{r['filename']}]\n{r['content']}" for r in results]
        return "\n\n---\n\n".join(parts)

    tools = [
        {
            "type": "function",
            "function": {
                "name": "search",
                "description": search.__doc__,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query string",
                        }
                    },
                    "required": ["query"],
                },
            },
        }
    ]

    system_prompt = (
        "You're a course teaching assistant. Answer the student's question using the "
        "search tool. Make multiple searches with different keywords before answering."
    )
    user_question = "How does the agentic loop work, and how is it different from plain RAG?"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]

    print("Q6 - Running agentic loop...")
    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            # Model stopped calling tools -> final answer
            print(f"Q6 - Final answer:\n{msg.content}")
            break

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"  -> Tool call: {func_name}(query='{args['query']}'")
            result = search(**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    print(f"Q6 - Number of search tool calls: {search_calls[0]}")
    return search_calls[0]


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("LLM Zoomcamp 2026 - Homework 1: Agentic RAG")
    print(f"Model: {MODEL} via OpenRouter")
    print("=" * 60)

    # Q1
    documents = load_documents()

    # Q2
    index = build_index(documents)
    q2_search(index)

    # Q3
    q3_tokens = q3_rag(index)

    # Q4
    chunks = q4_chunking(documents)

    # Q5
    chunk_index = q5_rag_with_chunks(chunks, q3_tokens)

    # Q6
    q6_agent(chunk_index)

    print("\n" + "=" * 60)
    print("All questions answered!")
    print("=" * 60)
