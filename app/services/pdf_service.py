from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


class PDFService:
    """Load PDF documents and extract page-level content."""

    @staticmethod
    def extract_document(file_path: Path) -> dict:
        """Extract PDF pages and basic metadata."""

        try:
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()

        except Exception as exc:
            raise ValueError("Unable to read or extract text from the PDF.") from exc

        pages = [
            {
                "page_number": document.metadata["page"] + 1,
                "text": document.page_content.strip(),
            }
            for document in documents
            if document.page_content.strip()
        ]

        total_characters = sum(len(page["text"]) for page in pages)

        if not total_characters:
            raise ValueError("No extractable text found in the PDF.")

        return {
            "pages": pages,
            "total_pages": len(documents),
            "total_characters": total_characters,
        }