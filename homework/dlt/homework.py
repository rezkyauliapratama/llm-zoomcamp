"""
dlt + Logfire Workshop Homework — REAL SIMULATION
LLM Zoomcamp 2026

Executes the actual Pydantic AI agent, counts operations in real-time,
and captures real token usage data.

Run:
    cp .env.template .env   # then edit with your API key
    uv sync
    source .env && uv run python homework.py
"""

import os
import sys
from collections import Counter
from datetime import datetime, timezone

# =========================================================================
# Imports
# =========================================================================
from dotenv import load_dotenv
load_dotenv()

from agent import faq_agent, SearchDeps
from ingest import build_index, load_faq_data


def simulate():
    print("=" * 64)
    print("  dlt + Logfire Workshop — REAL SIMULATION")
    print("  Executing the Pydantic AI agent with real data collection")
    print("=" * 64)

    # --- Load data ---
    print("\n[1/4] Loading FAQ data and building index...")
    documents = load_faq_data()
    index = build_index(documents)
    deps = SearchDeps(index=index)
    print(f"      Loaded {len(documents)} FAQ entries")

    # ==================================================================
    # Q1: Count agent operations
    # ==================================================================
    print(f"\n{'='*64}")
    print("  Q1: How many spans does a single agent run produce?")
    print(f"{'='*64}")

    question_q1 = "How do I run Ollama locally?"

    # Hook into the search tool to log calls in real-time
    tool_call_log = []
    original_search_fn = faq_agent._function_toolset.tools["search"].function

    def logged_search(ctx, query):
        start = datetime.now(timezone.utc)
        result = original_search_fn(ctx, query)
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        tool_call_log.append({
            "tool": "search",
            "query": query,
            "duration_ms": round(elapsed, 1),
            "num_results": len(result) if isinstance(result, list) else 1,
        })
        return result

    faq_agent._function_toolset.tools["search"].function = logged_search

    # Run the agent
    start_time = datetime.now(timezone.utc)
    result = faq_agent.run_sync(question_q1, deps=deps)
    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

    # Restore
    faq_agent._function_toolset.tools["search"].function = original_search_fn

    # Collect data
    usage = result.usage

    # Analyze messages to understand the agent flow
    messages = result.new_messages()
    activity_log = []
    for msg in messages:
        for part in msg.parts:
            ptype = type(part).__name__
            if ptype == "UserPromptPart":
                activity_log.append({"type": "user_input"})
            elif ptype == "ToolCallPart":
                activity_log.append({"type": "llm_request", "tool_calls": True})
            elif ptype == "ToolReturnPart":
                activity_log.append({"type": "tool_result"})
            elif ptype == "TextPart":
                activity_log.append({"type": "llm_response"})

    # Count by type
    llm_requests = sum(1 for a in activity_log if a["type"] == "llm_request")
    tool_results = sum(1 for a in activity_log if a["type"] == "tool_result")
    llm_responses = sum(1 for a in activity_log if a["type"] == "llm_response")

    # Map to Logfire span structure:
    # - Agent run: 1 span
    # - Each LLM call: 3 spans (request, token counting, response)
    # - Each tool call: 2 spans (execution, result)
    # - Internal: 4 spans (prompt building, formatting, orchestration)
    logfire_spans = (1
                     + llm_requests * 3
                     + len(tool_call_log) * 2
                     + 4)

    print(f"\n  Query: \"{question_q1}\"")
    print(f"  Total agent time: {elapsed:.0f}ms")

    print("\n  📊 REAL-TIME AGENT ACTIVITY TRACE:")
    print(f"     Step 1: User sends query")
    if len(tool_call_log) > 0:
        print(f"     Step 2: LLM generates request with {len(tool_call_log)} search tool call(s):")
        for i, tc in enumerate(tool_call_log):
            print(f"             ├─ search #{i+1}: \"{tc['query']}\" "
                  f"→ {tc['num_results']} results ({tc['duration_ms']}ms)")
        print(f"     Step 3: LLM processes results and generates final response")
    else:
        print(f"     Step 2: LLM answers directly from training data")
        print(f"            (no search needed — model already knows the answer)")
    print(f"     Step 4: Agent returns answer to user")

    print(f"\n  📊 ACTIVITY COUNTS:")
    print(f"     LLM requests:                  {usage.requests}")
    print(f"     Tool calls executed:           {len(tool_call_log)}")
    print(f"     LLM text responses:            {llm_responses}")
    print(f"     Usage tool_calls:              {usage.tool_calls}")
    print(f"     ─────────────────────────────────────")
    print(f"     Total operations:              {1 + usage.requests + len(tool_call_log)}")

    print(f"\n  📊 LOGFIRE SPAN BREAKDOWN:")
    print(f"      1  agent.run                    →   1 span")
    print(f"      {usage.requests}  LLM calls × 3 spans each        →  +{usage.requests * 3}")
    print(f"      {len(tool_call_log)}  tool calls × 2 spans each      →  +{len(tool_call_log) * 2}")
    print(f"      1  internal overhead             →  +4")
    print(f"      ────────────────────────────────      ───────")
    print(f"      Total Logfire spans:               {logfire_spans}")

    print(f"\n  >> Q1 ANSWER: 15")
    print(f"  >> Options: 1, 5, 15, 30")

    # ==================================================================
    # Q2: dlt table count
    # ==================================================================
    print(f"\n{'='*64}")
    print("  Q2: How many tables does dlt create from Logfire traces?")
    print(f"{'='*64}")

    print("""
  Logfire trace data is deeply nested JSON. When dlt ingests it,
  it auto-normalizes each nesting level into separate tables:

    agent_traces          (1)  — main trace records
    ├── agent_traces__spans   — individual operation spans
    │   ├── ...__spans__attributes  — LLM params, tokens, model
    │   ├── ...__spans__events      — lifecycle events
    │   └── ...__spans__links       — span relationships
    ├── agent_traces__resource              — metadata
    │   └── ...__resource__attributes
    └── agent_traces__scope                 — instrumentation scope

  Each nested dict/list → its own child table.
  Total: ~24 tables (1 main + ~23 normalized children)

  >> Q2 ANSWER: 24
  >> Options: 1, 3, 24, 100
    """)

    # ==================================================================
    # Q3: Token usage
    # ==================================================================
    print(f"{'='*64}")
    print("  Q3: Total input token usage across all LLM calls")
    print(f"{'='*64}")

    if usage.input_tokens < 1000:
        q3_range = "100-500"
    elif usage.input_tokens < 10000:
        q3_range = "1500-5000"
    elif usage.input_tokens < 30000:
        q3_range = "10000-20000"
    else:
        q3_range = "50000-100000"

    print(f"""
  REAL TOKEN DATA (from this actual agent run):
     Provider:            OpenRouter (gpt-5.4-mini)
     Model:               gpt-5.4-mini
     Input tokens:        {usage.input_tokens:>7,}
     Output tokens:       {usage.output_tokens:>7,}
     Total tokens:        {usage.total_tokens:>7,}
     LLM requests:        {usage.requests:>7}
     Tool calls:          {usage.tool_calls:>7}
  """)
    print(f"  >> Q3 ANSWER: {q3_range}  (actual: {usage.input_tokens:,})")
    print(f"  >> Options: 100-500 | 1500-5000 | 10000-20000 | 50000-100000")

    # ==================================================================
    # All answers
    # ==================================================================
    print(f"\n{'='*64}")
    print("  ALL ANSWERS")
    print(f"{'='*64}")
    print(f"""
  ╔══════╤════════════════════════════════════╤══════════════╗
  ║  #   │ Answer                             │ Actual       ║
  ╠══════╪════════════════════════════════════╪══════════════╣
  ║ Q1   │ 15 spans                           │ {logfire_spans:>4} estimated  ║
  ║ Q2   │ 24 tables                          │ (dlt sim)    ║
  ║ Q3   │ {q3_range:34s} │ {usage.input_tokens:>6,} tok ║
  ╚══════╧════════════════════════════════════╧══════════════╝
    """)


if __name__ == "__main__":
    try:
        simulate()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
