from fastapi import APIRouter

from app.helpers.chat_helper import ChatHelper
from app.schemas.chat_schema import ChatRequest, ChatResponse


chat_router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])


@chat_router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate an answer from uploaded documents."""

    return await ChatHelper.ask_question(
        question=request.question,
        top_k=request.top_k,
        document_id=request.document_id,
    )