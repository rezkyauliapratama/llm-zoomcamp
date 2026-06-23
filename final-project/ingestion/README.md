# Ingestion Pipeline

Document ingestion pipeline untuk OJK/BI regulatory documents.

## Overview

Pipeline menggunakan N8N untuk orchestrasi dan menjalankan flow berikut:

```
[Schedule Trigger (weekly)]
    → HTTP Request — Download PDFs from ojk.go.id / bi.go.id
    → Extract from File (N8N node) — PDF text extraction
    → Recursive Character Text Splitter (chunk_size=512, overlap=64)
    → Metadata Enrichment (source, pasal, bab, tahun, topik)
    → Embeddings Node (multilingual-e5-base)
    → PGVector Store (Insert Mode)
    → Log ingestion metadata to PostgreSQL
```

## Files

```
ingestion/
├── README.md
├── n8n-workflows/
│   └── ojk_ingestion_workflow.json   ← N8N workflow export (import via UI)
├── scripts/
│   ├── download_documents.py         ← manual download script
│   ├── chunk_documents.py            ← chunking logic (section-based)
│   └── ingest_to_pgvector.py         ← direct PGVector ingestion
└── data/
    └── documents/                    ← downloaded PDFs (gitignored)
```

## Priority Documents

| Document | Source | Type | Pages |
|----------|--------|------|-------|
| Panduan Tata Kelola AI Perbankan (2025) | ojk.go.id | Panduan | ~80 |
| Indonesia Banking Booklet 2025 | ojk.go.id | Statistik | ~150 |
| POJK No. 11/POJK.03/2022 (TI) | ojk.go.id | POJK | ~60 |
| POJK No. 18/POJK.03/2023 (Risiko) | ojk.go.id | POJK | ~90 |
| SE OJK - Manajemen Risiko TI | ojk.go.id | SE OJK | ~40 |
| Peraturan BI (GWM, Sistem Pembayaran) | bi.go.id | PBI | ~30 |

## Chunk Schema

```python
{
    "id": "uuid",
    "source_document": "POJK No. 11/POJK.03/2022",
    "document_type": "POJK",  # POJK | SE OJK | PBI | PADG | Panduan
    "pasal": "Pasal 15 Ayat 2",  # nullable
    "bab": "BAB III - Manajemen Risiko",  # nullable
    "tahun_terbit": "2022",
    "topik": "Manajemen Risiko TI",
    "bahasa": "id",  # id | en
    "content": "...",
    "char_count": 450
}
```

## Setup

```bash
# Install dependencies
pip install -r ../requirements.txt

# Download documents manually
python scripts/download_documents.py

# Or import N8N workflow for automated ingestion:
# N8N UI → Workflows → Import → select ojk_ingestion_workflow.json
```
