import os
from functools import lru_cache
from pathlib import Path

import chromadb

from app.config import settings

class VectorStoreService:
    """Manage document chunks and embeddings in ChromaDB."""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_collection():
        """Initialize the persistent ChromaDB collection."""

        base_directory = Path(__file__).resolve().parents[2]

        persist_directory = Path(settings.chroma_persist_directory)

        if not persist_directory.is_absolute():
            persist_directory = base_directory / persist_directory

        collection_name = settings.chroma_collection_name

        client = chromadb.PersistentClient(path=str(settings.chroma_persist_directory))

        return client.get_or_create_collection(
            name=collection_name,
            embedding_function=None,
            configuration={"hnsw": {"space": "cosine"}}
        )

    @classmethod
    def store_chunks(cls, document_id: str, filename: str, chunks: list, embeddings: list[list[float]]) -> int:
        """Store document chunks, embeddings, and metadata."""

        if not chunks:
            return 0

        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match.")

        collection = cls.get_collection()

        chunk_ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        documents = [chunk.page_content for chunk in chunks]

        metadatas = [
            {
                "document_id": document_id,
                "filename": filename,
                "page_number": chunk.metadata["page"],
            }
            for chunk in chunks
        ]

        collection.upsert(
            ids=chunk_ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(chunk_ids)

    @classmethod
    def delete_document_chunks(cls, document_id: str) -> int:
        collection = cls.get_collection()

        results = collection.get(
            where={"document_id": document_id},
            include=["metadatas"],
        )

        chunk_ids = results["ids"]

        if chunk_ids:
            collection.delete(ids=chunk_ids)

        return len(chunk_ids)