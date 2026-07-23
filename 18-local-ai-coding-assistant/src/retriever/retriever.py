import numpy as np

from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.faiss_store import FAISSStore


class Retriever:

    def __init__(self, store: FAISSStore):

        self.store = store

        self.embedding_generator = EmbeddingGenerator()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        query_embedding = self.embedding_generator.model.encode(
            [query],
            convert_to_numpy=True,
        )

        distances, indices = self.store.index.search(
            query_embedding.astype("float32"),
            top_k,
        )

        results = []

        for score, idx in zip(
            distances[0],
            indices[0],
        ):

            if idx == -1:
                continue

            results.append(
                (
                    self.store.metadata[idx],
                    float(score),
                )
            )

        return results