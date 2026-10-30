import os
from functools import lru_cache

from langchain_groq import ChatGroq

from app.config import settings
from app.prompts.rag_prompt import RAG_PROMPT

from app.config import settings


class LLMService:
    """Generate responses using Groq language models."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_model() -> ChatGroq:
        """Initialize and cache the Groq language model."""

        return ChatGroq(model=settings.groq_model, temperature=settings.llm_temperature, max_retries=2)

    @classmethod
    async def generate_answer(cls, question: str, context: str) -> str:
        """Generate an answer using the supplied context."""

        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not context.strip():
            raise ValueError("Context cannot be empty.")

        model = cls.get_model()

        messages = RAG_PROMPT.format_messages(
            context=context,
            question=question,
        )
        response = await model.ainvoke(messages)

        return str(response.content)