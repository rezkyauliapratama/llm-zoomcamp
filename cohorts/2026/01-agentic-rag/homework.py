#!/usr/bin/env python3
"""
Homework 01: Agentic RAG
LLM Zoomcamp 2026 - Module 01

Dataset  : DataTalksClub/llm-zoomcamp lesson pages (commit 8c1834d)
Search   : minsearch (simple in-memory full-text search)
LLM      : deepseek/deepseek-chat-v3-0324 via OpenRouter
"""

import json
import re
from dataclasses import dataclass
from typing import Callable

import minsearch
import requests
from gitsource import GithubRepositoryDataReader, chunk_documents

# ---------------------------------------------------------------------------
# CONFIG — paste your key here or set OPENROUTER_API_KEY env var
# ---------------------------------------------------------------------------
OPENROUTER_API_KEY = ""  # <-- put your key here
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324"  # deepseek-v3 "flash" on OpenRouter


# ===========================================================================
# SECTION 1 — Load dataset
# ===========================================================================

def load_documents() -> list[dict]:
    """Download lesson pages from the course repo at commit 8c1834d."""
    reader = GithubRepositoryDataReader(
        repo_owner="DataTalksClub",
        repo_name="llm-zoomcamp",
        commit_id="8c1834d",
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )
    files = reader.read()
    documents = [file.parse() for file in files]
    return documents


# ===========================================================================
# SECTION 2 — minsearch helpers
# ===========================================================================

def build_index(documents: list[dict]) -> minsearch.Index:
    """Build a minsearch index from documents."""
    index = minsearch.Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )
    index.fit(documents)
    return index


def search(index: minsearch.Index, query: str, num_results: int = 5) -> list[dict]:
    """Search the index and return top results."""
    return index.search(query, num_results=num_results)


# ===========================================================================
# SECTION 3 — OpenRouter LLM client
# ===========================================================================

@dataclass
class LLMUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass
class LLMResponse:
    content: str
    usage: LLMUsage


def call_llm(messages: list[dict], tools: list[dict] | None = None) -> LLMResponse:
    """
    Call DeepSeek via OpenRouter.
    Returns full response including token usage.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/rezkyauliapratama/llm-zoomcamp",
        "X-Title": "LLM Zoomcamp Homework 01",
    }

    payload: dict = {
        "model": MODEL,
        "messages": messages,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    resp = requests.post(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()

    choice = data["choices"][0]
    usage_raw = data.get("usage", {})
    usage = LLMUsage(
        input_tokens=usage_raw.get("prompt_tokens", 0),
        output_tokens=usage_raw.get("completion_tokens", 0),
        total_tokens=usage_raw.get("total_tokens", 0),
    )

    return LLMResponse(content=choice["message"]["content"] or "", usage=usage), choice["message"]


# ===========================================================================
# SECTION 4 — RAG pipeline
# ===========================================================================

def build_context(results: list[dict]) -> str:
    context_parts = []
    for doc in results:
        context_parts.append(
            f"filename: {doc['filename']}\n\n{doc['content']}"
        )
    return "\n\n---\n\n".join(context_parts)


def rag(index: minsearch.Index, query: str) -> tuple[str, LLMUsage]:
    """Single-shot RAG: search once, then answer."""
    results = search(index, query)
    context = build_context(results)

    prompt = (
        "You are a helpful course assistant.\n\n"
        "Answer the question below using ONLY the context provided.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}"
    )

    messages = [{"role": "user", "content": prompt}]
    (llm_resp, _raw) = call_llm(messages)
    return llm_resp.content, llm_resp.usage


# ===========================================================================
# SECTION 5 — Agentic RAG (Q6)
# ===========================================================================

def make_search_tool_schema() -> dict:
    return {
        "type": "function",
        "function": {
            "name": "search",
            "description": (
                "Search the course knowledge base of lesson pages. "
                "Returns relevant lesson content for a given query."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string.",
                    }
                },
                "required": ["query"],
            },
        },
    }


def run_agent(chunk_index: minsearch.Index, user_question: str) -> tuple[str, int]:
    """
    Agentic loop: LLM decides when to call search.
    Returns (final_answer, search_call_count).
    """
    system_prompt = (
        "You're a course teaching assistant. Answer the student's question using the "
        "search tool. Make multiple searches with different keywords before answering."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]

    tools = [make_search_tool_schema()]
    search_call_count = 0
    max_iterations = 20  # safety cap

    for _ in range(max_iterations):
        _response, raw_message = call_llm(messages, tools=tools)
        messages.append({"role": "assistant", **_format_assistant_message(raw_message)})

        tool_calls = raw_message.get("tool_calls") or []

        if not tool_calls:
            # No more tool calls → agent is done
            return raw_message.get("content", ""), search_call_count

        # Process each tool call
        for tc in tool_calls:
            fn_name = tc["function"]["name"]
            fn_args = json.loads(tc["function"]["arguments"])

            if fn_name == "search":
                search_call_count += 1
                query = fn_args["query"]
                results = search(chunk_index, query)
                context = build_context(results)
                tool_result = context if context else "No results found."
            else:
                tool_result = f"Unknown tool: {fn_name}"

            messages.append({
                "role": "tool",
                "tool_call_id": tc["id"],
                "content": tool_result,
            })

    return "Max iterations reached.", search_call_count


def _format_assistant_message(raw: dict) -> dict:
    """Strip keys not allowed in assistant turn."""
    msg = {"role": "assistant", "content": raw.get("content") or ""}
    if raw.get("tool_calls"):
        msg["tool_calls"] = raw["tool_calls"]
    return msg


# ===========================================================================
# MAIN — run all questions
# ===========================================================================

def main():
    print("=" * 60)
    print("LLM Zoomcamp 2026 — Homework 01: Agentic RAG")
    print("Model:", MODEL)
    print("=" * 60)

    # --- Load dataset ---
    print("\n[*] Loading lesson pages from GitHub (commit 8c1834d)...")
    documents = load_documents()

    # --- Q1 ---
    print(f"\nQ1. Number of lesson pages: {len(documents)}")

    # --- Q2 ---
    print("\n[*] Building minsearch index (full documents)...")
    index = build_index(documents)

    query_q2 = "How does the agentic loop keep calling the model until it stops?"
    results_q2 = search(index, query_q2)
    print(f"Q2. First result filename: {results_q2[0]['filename']}")

    # --- Q3 ---
    print("\n[*] Running RAG (Q3)...")
    answer_q3, usage_q3 = rag(index, query_q2)
    print(f"Q3. Input (prompt) tokens: {usage_q3.input_tokens}")
    print(f"    Answer snippet: {answer_q3[:200]}...")

    # --- Q4 ---
    print("\n[*] Chunking documents (size=2000, step=1000)...")
    chunks = chunk_documents(documents, size=2000, step=1000)
    print(f"Q4. Number of chunks: {len(chunks)}")

    # --- Q5 ---
    print("\n[*] Building minsearch index (chunks)...")
    chunk_index = build_index(chunks)

    print("[*] Running RAG with chunked index (Q5)...")
    answer_q5, usage_q5 = rag(chunk_index, query_q2)
    ratio = usage_q3.input_tokens / max(usage_q5.input_tokens, 1)
    print(f"Q5. Input tokens (chunked): {usage_q5.input_tokens}")
    print(f"    Input tokens (full doc): {usage_q3.input_tokens}")
    print(f"    Ratio (full / chunked):  {ratio:.1f}x fewer")

    # --- Q6 ---
    print("\n[*] Running Agentic RAG (Q6)...")
    query_q6 = "How does the agentic loop work, and how is it different from plain RAG?"
    final_answer, search_calls = run_agent(chunk_index, query_q6)
    print(f"Q6. Number of search tool calls: {search_calls}")
    print(f"    Final answer snippet: {final_answer[:300]}...")

    print("\n" + "=" * 60)
    print("Done! Fill in the answers at:")
    print("https://courses.datatalks.club/llm-zoomcamp-2026/homework/hw1")
    print("=" * 60)


if __name__ == "__main__":
    main()
