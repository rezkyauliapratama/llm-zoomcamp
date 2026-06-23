"""Script to download OJK/BI regulatory documents for ingestion.

Usage:
    python download_documents.py

Documents are saved to ../data/raw/
"""

import os
import requests
from pathlib import Path

# Base directories
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Priority documents to download
# TODO: Add actual OJK/BI document URLs after verifying availability
DOCUMENTS = [
    {
        "name": "panduan_tata_kelola_ai_2025",
        "url": "https://ojk.go.id/...",  # Replace with actual URL
        "type": "Panduan",
        "year": "2025",
    },
    {
        "name": "pojk_11_2022_teknologi_informasi",
        "url": "https://ojk.go.id/...",  # Replace with actual URL
        "type": "POJK",
        "year": "2022",
    },
    # Add more documents here
]


def download_document(doc: dict) -> None:
    """Download a single regulatory document."""
    output_path = RAW_DATA_DIR / f"{doc['name']}.pdf"
    if output_path.exists():
        print(f"[SKIP] {doc['name']} already exists")
        return

    print(f"[DOWNLOAD] {doc['name']}...")
    try:
        response = requests.get(doc["url"], timeout=60)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        print(f"[OK] Saved to {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to download {doc['name']}: {e}")


if __name__ == "__main__":
    for doc in DOCUMENTS:
        download_document(doc)
    print(f"\nAll documents saved to: {RAW_DATA_DIR}")
