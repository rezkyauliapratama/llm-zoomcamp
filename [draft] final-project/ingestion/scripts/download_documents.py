"""Manual document download script for OJK/BI regulatory documents."""
import os
import requests
from pathlib import Path

DOCUMENTS = [
    # Add OJK document URLs here
    # Format: (url, filename, document_type, year)
    # Example:
    # ("https://ojk.go.id/path/to/document.pdf", "panduan_ai_2025.pdf", "Panduan", "2025"),
]

OUTPUT_DIR = Path("data/documents")


def download_document(url: str, filename: str) -> bool:
    """Download a single document."""
    output_path = OUTPUT_DIR / filename
    if output_path.exists():
        print(f"[SKIP] {filename} already exists")
        return True

    print(f"[DOWNLOAD] {filename}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        print(f"[OK] {filename} ({len(response.content) / 1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        return False


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for url, filename, doc_type, year in DOCUMENTS:
        download_document(url, filename)
    print("\nDownload complete.")
