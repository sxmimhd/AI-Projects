from pathlib import Path

import pandas as pd

from src.utils.logger import Logger


class DatasetLoader:

    def __init__(self, dataset_path: Path):
        self.dataset_path = Path(dataset_path)
        self.logger = Logger.get_logger()
        self.dataframe = None

    def load(self) -> pd.DataFrame:
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found:\n{self.dataset_path}"
            )

        self.dataframe = pd.read_csv(
            self.dataset_path,
            low_memory=False
        )

        self.logger.info(
            f"Dataset loaded successfully ({len(self.dataframe):,} rows)."
        )

        return self.dataframe

    def get_shape(self) -> tuple[int, int]:
        self._ensure_loaded()
        return self.dataframe.shape

    def get_columns(self) -> list[str]:
        self._ensure_loaded()
        return self.dataframe.columns.tolist()

    def get_memory_usage(self) -> float:
        self._ensure_loaded()
        return self.dataframe.memory_usage(deep=True).sum() / (1024 ** 2)

    def get_duplicate_count(self) -> int:
        self._ensure_loaded()
        return int(self.dataframe.duplicated().sum())

    def preview(self, rows: int = 5) -> pd.DataFrame:
        self._ensure_loaded()
        return self.dataframe.head(rows)

    def _ensure_loaded(self):
        if self.dataframe is None:
            raise ValueError(
                "Dataset has not been loaded yet."
            )