from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings

class TextChunkingService:
    """Split documents into smaller chunks."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
        )

    def split_pages(self, pages: list[dict]) -> list[Document]:
        """Split PDF pages while preserving their metadata."""

        documents = [
            Document(
                page_content=page["text"],
                metadata={"page": page["page_number"]},
            )
            for page in pages
        ]

        return self.text_splitter.split_documents(documents)