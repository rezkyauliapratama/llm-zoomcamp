# 🖥️ Interface Layer — Open WebUI

Open WebUI serves as the primary chat interface. Two integration patterns with N8N:

## Pattern 1: N8N as Ingestion-Only (Phase 1 - MVP)

Open WebUI uses its built-in RAG pipeline connected to the same PGVector database.
N8N only handles document ingestion.

**Pros:** Fastest to MVP. Open WebUI handles RAG natively.

## Pattern 2: N8N as Full RAG Pipeline (Phase 2)

Open WebUI forwards all chat messages to an N8N webhook via the Pipeline Function.
N8N runs the full RAG agentic loop (rewrite → hybrid → rerank → generate).

See `open_webui_pipeline.py` for the Pipeline function implementation.

## Files

| File | Description |
|------|-------------|
| `open_webui_pipeline.py` | Open WebUI Pipeline function — forwards to N8N webhook |
| `n8n_rag_workflow.json` | N8N workflow export for full RAG query flow |

## Open WebUI Admin Configuration

1. Admin Panel → Settings → Documents:
   - Enable Hybrid Search
   - Set Top K = 10, Top K Reranker = 5
   - Configure embedding model: `intfloat/multilingual-e5-base`

2. Workspace → Knowledge:
   - Create Knowledge Base: "OJK/BI Regulatory Documents"
   - Upload PDFs or point to PGVector collection

3. Workspace → Models:
   - Create custom model "OJK Regulatory Assistant"
   - Attach Knowledge Base + System Prompt V2
