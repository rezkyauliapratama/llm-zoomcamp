# Monitoring

Grafana dashboard dan PostgreSQL schema untuk conversation logging.

## Files

```
monitoring/
├── README.md
├── sql/
│   └── schema.sql                          ← conversations + chunks table DDL
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── postgres.yaml               ← auto-provision PG datasource
│   │   └── dashboards/
│   │       └── dashboard.yaml              ← auto-provision dashboard config
│   └── dashboards/
│       └── ojk_rag_dashboard.json          ← main Grafana dashboard JSON
└── feedback_api.py                         ← endpoint to receive UI feedback
```

## PostgreSQL Schema: `conversations` Table

```sql
id              UUID         PRIMARY KEY
question        TEXT         User's original question
answer          TEXT         LLM-generated answer
model           TEXT         LLM model used
prompt_version  TEXT         'v1' or 'v2'
input_tokens    INTEGER
output_tokens   INTEGER
cost            NUMERIC      Cost in USD
source_docs     JSONB        [{source_document, pasal}]
feedback        TEXT         'thumbs_up' | 'thumbs_down' | NULL
judge_score     TEXT         'good' | 'bad' | 'neutral' | NULL
created_at      TIMESTAMPTZ  Auto-set
```

## Grafana Dashboard — 5 Required Charts

| # | Chart | Type |
|---|-------|------|
| 1 | Query volume per day | Bar/Time Series |
| 2 | Avg cost per query (rolling 7d) | Time Series |
| 3 | Feedback ratio over time | Stacked Bar |
| 4 | LLM judge score distribution | Pie/Donut |
| 5 | Top queried regulatory documents | Horizontal Bar |

## Access

- Grafana: http://localhost:3001
- Default credentials: see `.env.example`
