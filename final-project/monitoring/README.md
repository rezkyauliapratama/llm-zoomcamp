# Monitoring & Observability

PostgreSQL-backed conversation logging + Grafana dashboard with 5+ charts.

## PostgreSQL Schema

```sql
CREATE TABLE conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question        TEXT NOT NULL,
    answer          TEXT NOT NULL,
    model           TEXT,
    prompt_version  TEXT,  -- 'v1' or 'v2'
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    cost            NUMERIC(10, 6),
    source_docs     JSONB,  -- [{source_document, pasal}]
    feedback        TEXT,   -- 'thumbs_up' | 'thumbs_down' | NULL
    judge_score     TEXT,   -- 'good' | 'bad' | 'neutral' | NULL
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

## Grafana Dashboard Charts (5 required)

| # | Chart | Type | SQL Concept |
|---|-------|------|-------------|
| 1 | Query volume per day | Bar/Time Series | `GROUP BY DATE(created_at)` |
| 2 | Avg cost per query (rolling 7d) | Time Series | `AVG(cost)` with time window |
| 3 | Feedback ratio over time | Stacked Bar | `COUNT FILTER feedback` |
| 4 | LLM judge score distribution | Pie/Donut | `COUNT GROUP BY judge_score` |
| 5 | Top queried regulatory documents | Horizontal Bar | `jsonb_array_elements` |

Optional additional charts:
- Average token count per day
- Query latency percentiles (P50, P95)
- Cost accumulation over project duration
