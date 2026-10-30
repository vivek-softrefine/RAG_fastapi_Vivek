from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService

from app.config import settings

class RAGService:
    """Coordinate retrieval and LLM response generation."""

    @staticmethod
    def build_context(chunks: list[dict]) -> str:
        """Build document context from retrieved chunks."""

        context_parts = []

        for index, chunk in enumerate(chunks, start=1):
            metadata = chunk["metadata"]

            context_parts.append(
                f"""
                Source {index}:
                Filename: {metadata["filename"]}
                Page: {metadata["page_number"]}
                Content: {chunk["content"]}
                """
            )

        return "\n".join(context_parts)

    @classmethod
    async def ask_question(cls, question: str, top_k: int | None = None, document_id: str | None = None) -> dict:
        """Retrieve relevant context and generate an answer."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        retrieved_chunks = RetrievalService.search_chunks(
            query=question,
            top_k=settings.retrieval_top_k,
            document_id=document_id,
        )

        if not retrieved_chunks:
            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the uploaded documents."
                ),
                "sources": [],
            }

        context = cls.build_context(retrieved_chunks)

        answer = await LLMService.generate_answer(question=question, context=context)

        sources = []
        seen_sources = set()

        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]

            source_key = (
                metadata["document_id"],
                metadata["page_number"],
            )

            if source_key in seen_sources:
                continue

            seen_sources.add(source_key)

            sources.append({
                "document_id": metadata["document_id"],
                "filename": metadata["filename"],
                "page_number": metadata["page_number"],
            })

        return {
            "answer": answer,
            "sources": sources,
        }