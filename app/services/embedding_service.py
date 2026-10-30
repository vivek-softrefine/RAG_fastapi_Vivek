from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings

class EmbeddingService:
    """Generate vector embeddings for text."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_model() -> SentenceTransformer:
        """Load and cache the embedding model."""

        return SentenceTransformer(settings.embedding_model_name)

    @classmethod
    def generate_embeddings(cls, texts: list[str]) -> list[list[float]]:
        """Generate normalized embeddings for a list of texts."""

        if not texts:
            return []

        model = cls.get_model()

        embeddings = model.encode(
            texts,
            batch_size=32,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.tolist()