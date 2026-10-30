import logging
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.services.pdf_service import PDFService

logger = logging.getLogger(__name__)


class DocumentHelper:
    """Handle document upload operations."""

    UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    @staticmethod
    async def upload_document(file: UploadFile) -> dict:
        """Validate, save and extract text from an uploaded PDF."""

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        file_content = await file.read(DocumentHelper.MAX_FILE_SIZE + 1)

        if len(file_content) > DocumentHelper.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds the 10 MB limit.",
            )

        if not file_content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file.",
            )

        document_id = str(uuid4())

        DocumentHelper.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        file_path = DocumentHelper.UPLOAD_DIR / f"{document_id}.pdf"
        file_path.write_bytes(file_content)

        try:
            extracted_document = PDFService.extract_document(file_path)
        except ValueError as exc:
            file_path.unlink(missing_ok=True)

            raise HTTPException(status_code=400, detail=str(exc)) from exc

        logger.info(
            "PDF processed | document_id=%s | filename=%s | characters=%s",
            document_id,
            file.filename,
            extracted_document["total_characters"],
        )

        return {
            "message": "Document uploaded and text extracted successfully.",
            "document": {
                "document_id": document_id,
                "filename": file.filename,
                "file_size": len(file_content),
                "content_type": "application/pdf",
                "status": "text_extracted",
                "uploaded_at": datetime.now(timezone.utc),
                "total_pages": extracted_document["total_pages"],
                "total_characters": extracted_document["total_characters"],
            },
        }