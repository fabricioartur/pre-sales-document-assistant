from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


class PdfExtractionError(RuntimeError):
    """Raised when a PDF cannot be read or contains no extractable text."""


def extract_text_from_pdf(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise PdfExtractionError(f"PDF file not found: {pdf_path}")

    if not pdf_path.is_file():
        raise PdfExtractionError(f"Path is not a file: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise PdfExtractionError("Input file must be a PDF.")

    try:
        reader = PdfReader(str(pdf_path))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:  # pypdf raises several exception types.
        raise PdfExtractionError(f"Could not extract text from PDF: {exc}") from exc

    text = "\n\n".join(page.strip() for page in pages if page.strip()).strip()
    if not text:
        raise PdfExtractionError("PDF has no extractable text.")

    return text
