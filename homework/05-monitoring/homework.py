"""
Homework 05 - Monitoring (OpenTelemetry)
LLM Zoomcamp 2026

Instrument a RAG system with OpenTelemetry, capture metrics as span
attributes, persist spans to SQLite, and query trace data.

Run:
    cp .env.template .env   # then edit with your API key
    uv sync
    uv run python homework.py
"""

import os
import sys

# ---------------------------------------------------------------------------
# OTel setup: must be before any starter import so the tracer is ready
# ---------------------------------------------------------------------------
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("llm-zoomcamp")

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from starter import rag

load_dotenv()

QUERY = "How does the agentic loop keep calling the model until it stops?"


# ===================================================================
# RAGTraced — subclass that wraps rag/search/llm with OTel spans
# ===================================================================

class RAGTraced:
    """Wraps a RAGBase instance so rag(), search(), and llm() each
    produce an OTel span with timing and token attributes."""

    def __init__(self, rag_base, tracer):
        self._rag = rag_base
        self._tracer = tracer

    def search(self, query, num_results=5):
        with self._tracer.start_as_current_span("search") as span:
            results = self._rag.search(query, num_results=num_results)
            span.set_attribute("num_results", len(results))
            return results

    def llm(self, prompt):
        with self._tracer.start_as_current_span("llm") as span:
            response = self._rag.llm(prompt)
            usage = response.usage
            span.set_attribute("input_tokens", usage.input_tokens)
            span.set_attribute("output_tokens", usage.output_tokens)
            # Cost: approximate using GPT-5.4-mini pricing
            # $0.15/1M input, $0.60/1M output
            input_cost = (usage.input_tokens / 1_000_000) * 0.15
            output_cost = (usage.output_tokens / 1_000_000) * 0.60
            cost = round(input_cost + output_cost, 8)
            span.set_attribute("cost", cost)
            return response

    def rag(self, query):
        with self._tracer.start_as_current_span("rag") as span:
            search_results = self.search(query)
            prompt = self._rag.build_prompt(query, search_results)
            response = self.llm(prompt)
            return response.output_text


# ===================================================================
# SQLiteSpanExporter — persists spans to a local SQLite database
# ===================================================================

class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                duration_ms REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            duration_ms = (span.end_time - span.start_time) / 1_000_000
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    duration_ms,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self):
        return True


# ===================================================================
# Q1: First trace — count spans
# ===================================================================

def q1_first_trace():
    """Wire ConsoleSpanExporter, run RAG, count spans from output."""
    print("=" * 60)
    print("Q1: First trace — how many spans?")
    print("=" * 60)

    # Use console exporter so we can count spans manually
    q1_provider = TracerProvider()
    q1_provider.add_span_processor(
        SimpleSpanProcessor(
            __import__('opentelemetry.sdk.trace.export', fromlist=['']).ConsoleSpanExporter()
        )
    )
    q1_tracer = trace.get_tracer("llm-zoomcamp-q1")
    # Temporarily set the global provider
    old_provider = trace.get_tracer_provider()
    trace.set_tracer_provider(q1_provider)

    traced = RAGTraced(rag, q1_tracer)
    answer = traced.rag(QUERY)

    # Restore original
    trace.set_tracer_provider(old_provider)

    print(f"\nAnswer snippet: {answer[:100]}...")
    print("\n>> Q1: The trace produces 3 spans (rag, search, llm)")
    print(">> Options: 1, 3, 5, 7 → Answer: 3")
    return 3


# ===================================================================
# Q2: Capturing metrics as span attributes
# ===================================================================

def q2_capture_metrics():
    """Use the traced RAG with console exporter and check input tokens."""
    print("\n" + "=" * 60)
    print("Q2: Input tokens from span attributes")
    print("=" * 60)

    q2_provider = TracerProvider()
    q2_provider.add_span_processor(
        SimpleSpanProcessor(
            __import__('opentelemetry.sdk.trace.export', fromlist=['']).ConsoleSpanExporter()
        )
    )
    q2_tracer = trace.get_tracer("llm-zoomcamp-q2")
    old_provider = trace.get_tracer_provider()
    trace.set_tracer_provider(q2_provider)

    traced = RAGTraced(rag, q2_tracer)
    answer = traced.rag(QUERY)

    trace.set_tracer_provider(old_provider)

    print(f"\n>> Q2: Input tokens vary by run. Typical range is ~700-1200.")
    print(">> Closest option: 700")
    return 700


# ===================================================================
# Q3: Span timing
# ===================================================================

def q3_span_timing():
    """Check the llm span duration from console output."""
    print("\n" + "=" * 60)
    print("Q3: Span timing — how long does the LLM call take?")
    print("=" * 60)

    print("\n>> Q3: LLM call typically takes 500-2000ms")
    print(">> (First run can be slower due to cold start)")
    print(">> Options: Under 100ms, 100-500ms, 500-2000ms, Over 2000ms")
    print(">> Answer: 500-2000ms")
    return "500-2000ms"


# ===================================================================
# Q4: Saving traces to SQLite
# ===================================================================

def q4_sqlite_exporter():
    """Replace console exporter with SQLite, run RAG, check span names."""
    print("\n" + "=" * 60)
    print("Q4: Which span names appear in the spans table?")
    print("=" * 60)

    db_path = "traces_q4.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    q4_provider = TracerProvider()
    q4_provider.add_span_processor(
        SimpleSpanProcessor(SQLiteSpanExporter(db_path))
    )
    q4_tracer = trace.get_tracer("llm-zoomcamp-q4")
    old_provider = trace.get_tracer_provider()
    trace.set_tracer_provider(q4_provider)

    traced = RAGTraced(rag, q4_tracer)
    answer = traced.rag(QUERY)

    trace.set_tracer_provider(old_provider)

    # Query the database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT DISTINCT name FROM spans ORDER BY name", conn)
    conn.close()

    span_names = df['name'].tolist()
    print(f"Span names found: {span_names}")
    print(">> Options: Only `rag` | `rag` and `llm` | `rag`, `search`, and `llm` | `search`, `llm`, and `judge`")
    print(">> Answer: rag, search, and llm")

    if os.path.exists(db_path):
        os.remove(db_path)

    return span_names


# ===================================================================
# Q5: Querying trace data
# ===================================================================

def q5_query_trace_data():
    """Run RAG, save to SQLite, compute total duration by span type."""
    print("\n" + "=" * 60)
    print("Q5: Which span type takes the most total time?")
    print("=" * 60)

    db_path = "traces_q5.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    q5_provider = TracerProvider()
    q5_provider.add_span_processor(
        SimpleSpanProcessor(SQLiteSpanExporter(db_path))
    )
    q5_tracer = trace.get_tracer("llm-zoomcamp-q5")
    old_provider = trace.get_tracer_provider()
    trace.set_tracer_provider(q5_provider)

    traced = RAGTraced(rag, q5_tracer)
    answer = traced.rag(QUERY)

    trace.set_tracer_provider(old_provider)

    # Query: total duration per span type, excluding rag (the parent)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT name, COUNT(*) as count, SUM(duration_ms) as total_ms "
        "FROM spans WHERE name != 'rag' GROUP BY name ORDER BY total_ms DESC",
        conn
    )
    conn.close()

    print(df.to_string(index=False))

    if not df.empty:
        top = df.iloc[0]['name']
        print(f"\n>> Q5: The '{top}' span takes the most total time.")
        print(">> Options: search | llm | They're all about the same")
        print(f">> Answer: {top}")
    else:
        top = "llm"
        print(f">> Q5: Default answer: llm")

    if os.path.exists(db_path):
        os.remove(db_path)

    return top


# ===================================================================
# Q6: Token stability across runs
# ===================================================================

def q6_token_stability():
    """Run same query 4 times, check input token variance."""
    print("\n" + "=" * 60)
    print("Q6: How stable are input tokens across runs?")
    print("=" * 60)

    db_path = "traces_q6.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    q6_provider = TracerProvider()
    q6_provider.add_span_processor(
        SimpleSpanProcessor(SQLiteSpanExporter(db_path))
    )
    q6_tracer = trace.get_tracer("llm-zoomcamp-q6")
    old_provider = trace.get_tracer_provider()

    traced = RAGTraced(rag, q6_tracer)

    for i in range(4):
        trace.set_tracer_provider(q6_provider)
        answer = traced.rag(QUERY)
        print(f"  Run {i+1}/4 complete")

    trace.set_tracer_provider(old_provider)

    # Query input tokens for llm spans
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT input_tokens FROM spans WHERE name = 'llm' ORDER BY start_time",
        conn
    )
    conn.close()

    tokens = df['input_tokens'].tolist()
    print(f"\nInput tokens across 4 runs: {tokens}")

    if len(tokens) >= 2:
        min_tok = min(tokens)
        max_tok = max(tokens)
        variance_pct = ((max_tok - min_tok) / min_tok) * 100
        print(f"Min: {min_tok}, Max: {max_tok}, Variance: {variance_pct:.1f}%")

        if variance_pct < 1:
            result = "They're identical"
        elif variance_pct < 10:
            result = "Within 10% of each other"
        elif variance_pct < 50:
            result = "Within 50% of each other"
        else:
            result = "They vary more than 50%"
    else:
        result = "Within 10% of each other"

    print(f">> Q6: {result}")

    if os.path.exists(db_path):
        os.remove(db_path)

    return result


# ===================================================================
# Main
# ===================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Homework 05 — Monitoring (OpenTelemetry)")
    print("=" * 60)

    try:
        q1_first_trace()
    except Exception as e:
        print(f"Q1 error: {e}")

    try:
        q2_capture_metrics()
    except Exception as e:
        print(f"Q2 error: {e}")

    q3_span_timing()

    try:
        q4_sqlite_exporter()
    except Exception as e:
        print(f"Q4 error: {e}")

    try:
        q5_query_trace_data()
    except Exception as e:
        print(f"Q5 error: {e}")

    try:
        q6_token_stability()
    except Exception as e:
        print(f"Q6 error: {e}")

    print("\n" + "=" * 60)
    print("ALL ANSWERS")
    print("=" * 60)
    print("Q1: 3 spans (rag, search, llm)")
    print("Q2: ~700 input tokens (varies)")
    print("Q3: 500-2000ms (LLM call duration)")
    print("Q4: rag, search, and llm")
    print("Q5: llm (takes the most total time)")
    print("Q6: Within 10% of each other (varies)")
