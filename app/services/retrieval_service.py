from app.services.embedding_service import EmbeddingService
from app.services.vectorstore_service import VectorStoreService

from app.config import settings

class RetrievalService:
    """Retrieve relevant document chunks using semantic search."""

    @staticmethod
    def search_chunks(query: str, top_k: int | None = None, document_id: str | None = None) -> list[dict]:
        """Search for the most relevant document chunks."""

        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        top_k = settings.retrieval_top_k if top_k is None else top_k

        if top_k < 1:
            raise ValueError("top_k must be greater than zero.")

        collection = VectorStoreService.get_collection()

        total_chunks = collection.count()

        if total_chunks == 0:
            return []

        query_embedding = EmbeddingService.generate_embeddings([query])[0]

        search_parameters = {
            "query_embeddings": [query_embedding],
            "n_results": min(top_k, total_chunks),
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        }

        if document_id:
            search_parameters["where"] = {"document_id": document_id}

        results = collection.query(**search_parameters)

        retrieved_chunks = []

        for index, chunk_id in enumerate(results["ids"][0]):
            retrieved_chunks.append({
                "chunk_id": chunk_id,
                "content": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": results["distances"][0][index],
            })

        return retrieved_chunks