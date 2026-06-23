# N8N Workflows

This directory contains exported N8N workflow JSON files for the OJK RAG ingestion pipeline.

## Workflows

| File | Description |
|------|-------------|
| `01-ingestion-scheduled.json` | Weekly scheduled ingestion of OJK/BI PDFs |
| `02-rag-query-pipeline.json` | Full RAG query flow (Pattern 2 — Phase 2) |
| `03-reingestion-webhook.json` | Manual trigger for on-demand re-ingestion |

## Import Instructions

1. Open N8N at `http://localhost:5678`
2. Go to **Workflows → Import from File**
3. Select the JSON file from this directory
4. Configure credentials (OpenAI API key, PostgreSQL connection)
5. Activate the workflow

## Key Nodes Used

- `Schedule Trigger` — weekly re-ingestion
- `HTTP Request` — download PDFs from ojk.go.id / bi.go.id
- `Extract from File` — PDF text extraction
- `Recursive Character Text Splitter` — chunking
- `Embeddings` (OpenAI / multilingual-e5) — vector generation
- `PGVector Store` (Insert Mode) — store to PostgreSQL
- `AI Agent` — agentic loop for query flow (Phase 2)
- `Webhook` — Open WebUI integration
