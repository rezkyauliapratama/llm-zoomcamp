"""Orchestration pipeline for ingesting OJK/BI regulatory documents.

Run with: python pipeline/ingestion_pipeline.py
Or schedule via Mage/Prefect for automated updates.
"""


def run_ingestion_pipeline():
    """Full ingestion: load → chunk → embed → index."""
    print("[1/4] Loading documents from data/raw/...")
    # TODO: load_pdf / load_html from src/ingestion/loader.py

    print("[2/4] Chunking documents...")
    # TODO: chunk_recursive from src/ingestion/chunker.py

    print("[3/4] Generating embeddings...")
    # TODO: get_embeddings from src/ingestion/embedder.py

    print("[4/4] Indexing into Qdrant + Elasticsearch...")
    # TODO: index_documents from src/retrieval/

    print("✅ Ingestion complete.")


if __name__ == "__main__":
    run_ingestion_pipeline()
