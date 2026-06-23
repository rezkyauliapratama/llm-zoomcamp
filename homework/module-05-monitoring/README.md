# Module 05 - Monitoring: Homework

> **Source:** [DataTalksClub/llm-zoomcamp/cohorts/2026/05-monitoring/](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/cohorts/2026)

## Overview

Modul ini mencakup setup monitoring dan observability untuk LLM applications.

**Key Topics:**
- PostgreSQL conversation logging schema
- Grafana dashboard setup (5+ charts)
- User feedback collection (thumbs up/down)
- Built-in LLM judge scoring
- Token cost tracking

## Files Structure

```
module-05-monitoring/
├── README.md               ← this file
├── notebook.ipynb          ← main homework notebook
├── docker-compose.yaml     ← PostgreSQL + Grafana
├── grafana/
│   └── dashboards/
│       └── rag_dashboard.json ← provisioned Grafana dashboard
├── sql/
│   └── schema.sql          ← conversations table DDL
├── requirements.txt        ← pinned dependencies
└── answers.md              ← submitted answers
```

## Setup

```bash
cd homework/module-05-monitoring
docker-compose up -d
# Open Grafana at http://localhost:3001

uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```
