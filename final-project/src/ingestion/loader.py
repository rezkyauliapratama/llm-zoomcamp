"""Document loaders for OJK/BI regulatory documents (PDF, HTML)."""


def load_pdf(path: str) -> list[dict]:
    """Load a PDF and return a list of page dicts with 'text' and 'metadata'."""
    # TODO: implement with PyMuPDF or pdfplumber
    raise NotImplementedError


def load_html(url: str) -> list[dict]:
    """Load an HTML page and return structured text chunks."""
    # TODO: implement with BeautifulSoup
    raise NotImplementedError
