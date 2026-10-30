from fastapi import HTTPException

from app.services.rag_service import RAGService

from app.config import settings

class ChatHelper:
    """Handle chat request processing."""

    @staticmethod
    async def ask_question(question: str, top_k: int | None = None, document_id: str | None = None) -> dict:
        """Process a question using the RAG pipeline."""

        try:
            return await RAGService.ask_question(
                question=question,
                top_k=settings.retrieval_top_k,
                document_id=document_id
            )

        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc