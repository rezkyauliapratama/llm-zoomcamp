# Ingestion Pipeline

Automated pipeline to download, parse, chunk, embed, and store OJK/BI regulatory documents.

## Two Integration Patterns

### Pattern 1: N8N-Only (MVP — Phase 1)
N8N handles full ingestion (download → chunk → embed → PGVector). Open WebUI uses its built-in RAG pipeline pointing to the same database.

### Pattern 2: N8N + Custom Python Reranker (Phase 2)
N8N handles ingestion. Open WebUI connects to an N8N webhook for the full RAG query flow with custom reranking.

## Document Sources (Priority)

| Document | Source | Est. Pages | Type |
|----------|--------|------------|------|
| Panduan Tata Kelola AI Perbankan 2025 | ojk.go.id | ~80 | Panduan |
| Indonesia Banking Booklet 2025 | ojk.go.id | ~150 | Statistik |
| POJK No. 11/POJK.03/2022 (Teknologi Informasi) | ojk.go.id | ~60 | POJK |
| POJK No. 18/POJK.03/2023 (Manajemen Risiko) | ojk.go.id | ~90 | POJK |
| SE OJK Manajemen Risiko TI | ojk.go.id | ~40 | SE OJK |
| Peraturan BI (GWM, Sistem Pembayaran) | bi.go.id | ~30 | PBI |

## Chunk Schema

```json
{
  "id": "UUID",
  "source_document": "POJK No. 11/POJK.03/2022",
  "document_type": "POJK | SE OJK | PBI | PADG | Panduan",
  "pasal": "Pasal 15 Ayat 2",
  "bab": "BAB III - Manajemen Risiko",
  "tahun_terbit": "2022",
  "topik": "Manajemen Risiko TI",
  "bahasa": "id | en",
  "content": "...",
  "char_count": 450
}
```
