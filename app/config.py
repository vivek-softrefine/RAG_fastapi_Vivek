import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Store and validate application configuration."""

    embedding_model_name: str
    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int
    groq_api_key: str
    groq_model: str
    llm_temperature: float
    max_upload_size_mb: int
    chroma_persist_directory: str
    chroma_collection_name: str

    @classmethod
    def from_environment(cls):
        """Load configuration values from environment variables."""

        config = cls(
            embedding_model_name=os.getenv(
                "EMBEDDING_MODEL_NAME",
                "sentence-transformers/all-MiniLM-L6-v2",
            ),
            chunk_size=int(os.getenv("CHUNK_SIZE", "1000")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "200")),
            retrieval_top_k=int(os.getenv("RETRIEVAL_TOP_K", "5")),
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            groq_model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            max_upload_size_mb=int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")),
            chroma_persist_directory=os.getenv(
                "CHROMA_PERSIST_DIRECTORY", "chroma_data"
            ),
            chroma_collection_name=os.getenv(
                "CHROMA_COLLECTION_NAME", "knowledge_documents"
            ),
        )

        config.validate()
        return config

    def validate(self) -> None:
        """Validate configuration values."""

        if not self.embedding_model_name.strip():
            raise ValueError("EMBEDDING_MODEL_NAME cannot be empty.")

        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE must be greater than zero.")

        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be non-negative and smaller than CHUNK_SIZE."
            )

        if self.retrieval_top_k < 1:
            raise ValueError("RETRIEVAL_TOP_K must be at least 1.")

        if not 0.0 <= self.llm_temperature <= 2.0:
            raise ValueError("LLM_TEMPERATURE must be between 0 and 2.")

        if self.max_upload_size_mb <= 0:
            raise ValueError("MAX_UPLOAD_SIZE_MB must be greater than zero.")

        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

settings = AppConfig.from_environment()