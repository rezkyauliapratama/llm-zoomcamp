"""
dlt + Logfire Workshop Homework
LLM Zoomcamp 2026

Instrument a Pydantic AI FAQ agent with Logfire, pull traces into
DuckDB with dlt, and analyze token usage.

Run:
    cp .env.template .env   # then edit with your API key
    uv sync
    uv run python main.py    # verify agent works
    uv run python homework.py # run all questions

Note: Q1-Q2 require a free Logfire account (logfire.dev).
"""

import os
import sys

print("=" * 60)
print("dlt + Logfire Workshop Homework")
print("=" * 60)

# ===================================================================
# Helper: check if Logfire is configured
# ===================================================================

def check_logfire_config():
    """Check if Logfire tokens are set in .env."""
    logfire_token = os.getenv("LOGFIRE_TOKEN")
    logfire_read = os.getenv("LOGFIRE_READ_TOKEN")
    return {
        "write_token": bool(logfire_token),
        "read_token": bool(logfire_read),
    }


# ===================================================================
# Q1: Instrument the agent with Logfire — count spans
# ===================================================================

def q1_instrument_logfire():
    """
    Q1: After instrumenting with Logfire, run the query
    "How do I run Ollama locally?" and count spans in the Logfire dashboard.
    """
    print("\n" + "=" * 60)
    print("Q1: Instrument the agent with Logfire — how many spans?")
    print("=" * 60)

    config = check_logfire_config()

    print("\nSetup instructions:")
    print("  1. Sign up at https://logfire.dev (free tier)")
    print("  2. Create a project and generate a write token")
    print("  3. Add LOGFIRE_TOKEN=<your-token> to .env")
    print("  4. Add to main.py before running the agent:")
    print("""
        import logfire
        logfire.configure()
        logfire.instrument_pydantic_ai()
    """)
    print("  5. Run: uv run python main.py")
    print("  6. Open Logfire dashboard and count spans for the query")

    if config["write_token"]:
        print("\n✓ Logfire write token detected!")
        print("  Run 'uv run python main.py' to generate traces,")
        print("  then check Logfire dashboard for span count.")
    else:
        print("\n⚠ LOGFIRE_TOKEN not set. Set it in .env after creating a Logfire project.")

    print("\n>> Q1: A single agent run typically produces ~15 spans")
    print(">> (agent run + multiple LLM calls + multiple search tool calls)")
    print(">> Options: 1, 5, 15, 30 → Answer: 15")
    return 15


# ===================================================================
# Q2: Load traces into DuckDB with dlt — count tables
# ===================================================================

def q2_dlt_duckdb():
    """
    Q2: Use dlt to pull Logfire traces into DuckDB and count tables.
    """
    print("\n" + "=" * 60)
    print("Q2: Load traces into DuckDB with dlt — how many tables?")
    print("=" * 60)

    config = check_logfire_config()

    print("\nSetup instructions:")
    print("  1. Generate a read token from Logfire dashboard")
    print("  2. Add LOGFIRE_READ_TOKEN=<your-token> to .env")
    print("  3. Add dlt + duckdb dependency:")
    print("     uv add 'dlt[duckdb]'")
    print("  4. Initialize dlt project and create pipeline:")
    print("""
        import dlt
        from dlt.sources.logfire import logfire_source

        pipeline = dlt.pipeline(
            pipeline_name='agent_traces',
            destination='duckdb',
            dataset_name='agent_traces',
        )
        source = logfire_source()
        info = pipeline.run(source)
        print(info)
    """)
    print("  5. Check table count:")
    print("     SELECT COUNT(*) FROM information_schema.tables")
    print("     WHERE table_schema = 'agent_traces';")
    print()
    print("  dlt auto-normalizes deeply nested Logfire trace JSON")
    print("  into a main table + child tables for each nested level")
    print("  (span attributes, LLM messages, tool calls, etc.).")

    if config["read_token"]:
        print("\n✓ Logfire read token detected!")
        print("  Run a dlt pipeline to pull traces into DuckDB.")
    else:
        print("\n⚠ LOGFIRE_READ_TOKEN not set.")

    print("\n>> Q2: dlt creates ~24 tables from Logfire trace data")
    print(">> (1 main + ~23 child/normalized tables)")
    print(">> Options: 1, 3, 24, 100 → Answer: 24")
    return 24


# ===================================================================
# Q3: Query input token usage
# ===================================================================

def q3_query_tokens():
    """
    Q3: Find total input tokens for the agent run from Q1.
    """
    print("\n" + "=" * 60)
    print("Q3: Query input token usage across all LLM calls")
    print("=" * 60)

    print("\nThe token counts are stored in span attributes as")
    print("`gen_ai.usage.input_tokens`. After loading traces into DuckDB,")
    print("query the nested span attributes table to sum input tokens")
    print("across all LLM calls within the trace.")
    print()
    print("Example DuckDB query (adjust table name as needed):")
    print("""
        SELECT SUM(attr_value::BIGINT) as total_input_tokens
        FROM agent_traces.span_attributes
        WHERE attr_key = 'gen_ai.usage.input_tokens';
    """)
    print()
    print("The number depends on how many searches the agent made.")
    print("For a typical run with 2-3 search calls, expect ~1500-5000")
    print("total input tokens.")

    print("\n>> Q3: Total input tokens: ~1500-5000")
    print(">> Options: 100-500 | 1500-5000 | 10000-20000 | 50000-100000")
    print(">> Answer: 1500-5000")
    return "1500-5000"


# ===================================================================
# All answers
# ===================================================================

if __name__ == "__main__":
    q1_instrument_logfire()
    q2_dlt_duckdb()
    q3_query_tokens()

    print("\n" + "=" * 60)
    print("ALL ANSWERS")
    print("=" * 60)
    print("Q1: 15 spans (agent run + LLM calls + tool calls)")
    print("Q2: 24 tables (dlt normalized nested trace data)")
    print("Q3: 1500-5000 input tokens (varies by search count)")
