"""Section-based chunking for Indonesian regulatory documents (POJK/SE OJK/PBI).

Chunking strategy:
- Detect BAB headings (e.g., "BAB III - MANAJEMEN RISIKO")
- Detect Pasal headings (e.g., "Pasal 15", "Pasal 15 Ayat 2")
- Each Pasal becomes one or more chunks (target: 400-600 tokens)
- Fallback to recursive splitter for sections without Pasal markers
- Preserve metadata: pasal, bab, source_document, tahun_terbit
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Chunk:
    content: str
    source_document: str
    document_type: str
    pasal: Optional[str] = None
    bab: Optional[str] = None
    tahun_terbit: Optional[str] = None
    topik: Optional[str] = None
    bahasa: str = "id"
    char_count: int = field(init=False)

    def __post_init__(self):
        self.char_count = len(self.content)


# Regex patterns for Indonesian legal document structure
BAB_PATTERN = re.compile(r'^BAB\s+[IVXLCDM]+\s*[-–]?\s*.+', re.MULTILINE | re.IGNORECASE)
PASAL_PATTERN = re.compile(r'^Pasal\s+\d+', re.MULTILINE | re.IGNORECASE)
AYAT_PATTERN = re.compile(r'^\(\d+\)', re.MULTILINE)


def chunk_document(text: str, metadata: dict, chunk_size: int = 512, overlap: int = 64) -> list[Chunk]:
    """Chunk a regulatory document using section-based strategy.

    Args:
        text: Full extracted text of the document.
        metadata: Document-level metadata (source_document, document_type, etc.)
        chunk_size: Target chunk size in characters.
        overlap: Overlap in characters at section boundaries.

    Returns:
        List of Chunk objects with metadata attached.
    """
    # TODO: Implement section-based chunking
    # 1. Split by BAB headings to get major sections
    # 2. Within each BAB, split by Pasal headings
    # 3. For large Pasal, further split by Ayat or recursive splitter
    raise NotImplementedError("Chunking implementation pending")
