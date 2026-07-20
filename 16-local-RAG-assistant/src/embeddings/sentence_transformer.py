from pathlib import Path

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from config import settings
from src.core.document import Document
from src.utils.helpers import load_numpy, save_numpy
from src.utils.logger import Logger
from src.core.metadata import Metadata
from src.utils.helpers import save_pickle, load_pickle

class SentenceTransformerEmbedder:

    def __init__(self):
        self.logger = Logger.get_logger()
        self.device = self.get_device()
        self.model = None

    def get_device(self) -> str:
        return "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self) -> None:
        self.logger.info(
            f"Loading embedding model on {self.device.upper()}..."
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL_NAME,
            device=self.device
        )

        self.logger.info("Embedding model loaded successfully.")

    def generate_embeddings(
        self,
        documents: list[Document]
    ) -> np.ndarray:

        if self.model is None:
            raise RuntimeError("Embedding model has not been loaded.")

        texts = [document.document for document in documents]

        embeddings = []

        for start in tqdm(
            range(0, len(texts), settings.EMBEDDING_BATCH_SIZE),
            desc="Generating Embeddings"
        ):
            batch = texts[start:start + settings.EMBEDDING_BATCH_SIZE]

            batch_embeddings = self.model.encode(
                batch,
                convert_to_numpy=True,
                normalize_embeddings=settings.NORMALIZE_EMBEDDINGS,
                show_progress_bar=False
            )

            embeddings.append(batch_embeddings)

        embeddings = np.vstack(embeddings)

        self.logger.info(
            f"Generated embeddings with shape {embeddings.shape}."
        )

        return embeddings

    def attach_embeddings(
        self,
        documents: list[Document],
        embeddings: np.ndarray
    ) -> None:

        for document, embedding in zip(documents, embeddings):
            document.embedding = embedding

    def save_embeddings(
        self,
        embeddings: np.ndarray
    ) -> None:

        save_numpy(
            embeddings,
            Path(settings.EMBEDDINGS_PATH)
        )

        self.logger.info(
            f"Embeddings saved to {settings.EMBEDDINGS_PATH}"
        )

    def load_embeddings(self) -> np.ndarray:

        embeddings = load_numpy(
            Path(settings.EMBEDDINGS_PATH)
        )

        self.logger.info(
            f"Loaded embeddings with shape {embeddings.shape}"
        )

        return embeddings
    
    def save_metadata(
        self,
        documents: list[Document]
    ) -> None:

        metadata = [
            Metadata(
                game_id=document.game_id,
                title=document.title,
                metadata=document.metadata
            )
            for document in documents
        ]

        save_pickle(
            metadata,
            settings.METADATA_PATH
        )

        self.logger.info(
            f"Metadata saved to {settings.METADATA_PATH}"
        )

    def load_metadata(self):

        metadata = load_pickle(
            settings.METADATA_PATH
        )

        self.logger.info(
            f"Loaded {len(metadata):,} metadata records."
        )

        return metadata