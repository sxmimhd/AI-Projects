from pathlib import Path

import faiss
import numpy as np

from config import settings
from src.utils.logger import Logger


class FAISSVectorStore:

    def __init__(self):
        self.logger = Logger.get_logger()
        self.index = None

    def create(self, embeddings: np.ndarray) -> None:
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings.astype("float32"))

        self.logger.info(
            f"FAISS index created with {self.index.ntotal:,} vectors."
        )

    def save(self) -> None:
        if self.index is None:
            raise RuntimeError("FAISS index has not been created.")

        faiss.write_index(
            self.index,
            str(settings.FAISS_INDEX_PATH)
        )

        self.logger.info(
            f"FAISS index saved to {settings.FAISS_INDEX_PATH}"
        )

    def load(self) -> None:
        self.index = faiss.read_index(
            str(settings.FAISS_INDEX_PATH)
        )

        self.logger.info(
            f"Loaded FAISS index with {self.index.ntotal:,} vectors."
        )

    def exists(self) -> bool:
        return Path(settings.FAISS_INDEX_PATH).exists()

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = settings.TOP_K_RESULTS
    ) -> tuple[np.ndarray, np.ndarray]:

        if self.index is None:
            raise RuntimeError("FAISS index is not loaded.")

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k
        )

        return scores, indices