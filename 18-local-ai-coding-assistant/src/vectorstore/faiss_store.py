import pickle
from pathlib import Path

import faiss
import numpy as np

from src.models.code_chunk import CodeChunk


class FAISSStore:
    """
    Stores and retrieves code embeddings.
    """

    def __init__(self):

        self.index = None

        self.metadata = []

    def build(
        self,
        embeddings: np.ndarray,
        chunks: list[CodeChunk],
    ):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            embeddings.astype("float32")
        )

        self.metadata = chunks

    def save(
        self,
        index_path: Path,
        embeddings_path: Path,
        metadata_path: Path,
        embeddings: np.ndarray,
    ):

        faiss.write_index(
            self.index,
            str(index_path),
        )

        np.save(
            embeddings_path,
            embeddings,
        )

        with open(
            metadata_path,
            "wb",
        ) as file:

            pickle.dump(
                self.metadata,
                file,
            )

    def load(
        self,
        index_path: Path,
        metadata_path: Path,
    ):

        self.index = faiss.read_index(
            str(index_path)
        )

        with open(
            metadata_path,
            "rb",
        ) as file:

            self.metadata = pickle.load(file)