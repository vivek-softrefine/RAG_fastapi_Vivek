from fastapi import APIRouter, File, UploadFile

from app.helpers.document_helper import DocumentHelper
from app.schemas.document_schema import DocumentUploadResponse

doc_router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])

@doc_router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document."""

    return await DocumentHelper.upload_document(file)