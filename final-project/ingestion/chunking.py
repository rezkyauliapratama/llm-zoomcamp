"""Document chunking strategies for OJK regulatory documents."""

from typing import List, Dict


def chunk_by_paragraph(text: str, max_chunk_size: int = 512) -> List[str]:
    """Split text into chunks by paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def chunk_by_article(text: str) -> List[Dict]:
    """Split OJK regulatory text by article (Pasal) boundaries."""
    import re
    pattern = r"(Pasal \d+)"
    parts = re.split(pattern, text)
    chunks = []

    for i in range(1, len(parts), 2):
        article_title = parts[i]
        article_content = parts[i + 1] if i + 1 < len(parts) else ""
        chunks.append({
            "title": article_title,
            "content": article_content.strip(),
            "chunk": f"{article_title}\n{article_content.strip()}"
        })

    return chunks
