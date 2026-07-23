from sentence_transformers import SentenceTransformer
import numpy as np

from src.models.code_chunk import CodeChunk


class EmbeddingGenerator:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def generate(
        self,
        chunks: list[CodeChunk],
    ) -> np.ndarray:

        texts = [
            chunk.to_embedding_text()
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        return embeddings