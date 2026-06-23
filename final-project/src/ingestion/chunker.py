"""Chunking strategies for regulatory documents."""


def chunk_by_paragraph(text: str, max_tokens: int = 512) -> list[str]:
    """Split text into paragraph-level chunks, respecting max_tokens."""
    # TODO: implement semantic paragraph chunking
    raise NotImplementedError


def chunk_recursive(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Recursive character splitter with overlap."""
    # TODO: implement recursive splitter
    raise NotImplementedError
