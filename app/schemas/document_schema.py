from datetime import datetime

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Schema for document metadata."""

    document_id: str
    filename: str
    file_size: int = Field(ge=0, description="File size in bytes")
    content_type: str
    status: str
    uploaded_at: datetime
    total_pages: int = Field(ge=0)
    total_characters: int = Field(ge=0)
    total_chunks: int = Field(ge=0)


class DocumentUploadResponse(BaseModel):
    """Schema returned after document upload."""

    message: str
    document: DocumentResponse


class DocumentListResponse(BaseModel):
    """Schema for listing uploaded documents."""

    total: int
    documents: list[DocumentResponse]