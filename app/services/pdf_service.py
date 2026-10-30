from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError


class PDFService:
    """Extract text and metadata from PDF documents."""

    @staticmethod
    def extract_document(file_path: Path) -> dict:
        """Extract PDF text and basic metadata."""

        try:
            reader = PdfReader(file_path)

            if reader.is_encrypted:
                raise ValueError("Encrypted PDF files are not supported.")

            extracted_pages = []

            for page in reader.pages:
                page_text = page.extract_text() or ""

                if page_text.strip():
                    extracted_pages.append(page_text.strip())

            extracted_text = "\n\n".join(extracted_pages)

            if not extracted_text.strip():
                raise ValueError("No extractable text found in the PDF.")

            return {
                "text": extracted_text,
                "total_pages": len(reader.pages),
                "total_characters": len(extracted_text),
            }

        except PdfReadError as exc:
            raise ValueError("Unable to read the PDF file.") from exc