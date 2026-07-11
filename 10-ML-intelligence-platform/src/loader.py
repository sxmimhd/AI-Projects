from pathlib import Path

import pandas as pd

from config.constants import SUPPORTED_FILE_TYPES


class DatasetLoader:

    def __init__(self):

        self.dataset = None

        self.file_path = None
        self.file_name = None

        self.rows = 0
        self.columns = 0

        self.memory_usage = 0

        self.numeric_columns = []
        self.categorical_columns = []

    def load_csv(self, file_path) -> pd.DataFrame:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"{path} not found.")

        if path.suffix.lower() not in SUPPORTED_FILE_TYPES:
            raise ValueError("Unsupported file format.")

        self.dataset = pd.read_csv(path)

        self.file_path = path
        self.file_name = path.name

        self._extract_metadata()

        return self.dataset

    def _extract_metadata(self):

        self.rows = self.dataset.shape[0]

        self.columns = self.dataset.shape[1]

        self.memory_usage = (
            self.dataset.memory_usage(deep=True).sum()
            / (1024 ** 2)
        )

        self.numeric_columns = (
            self.dataset
            .select_dtypes(include="number")
            .columns
            .tolist()
        )

        self.categorical_columns = (
            self.dataset
            .select_dtypes(exclude="number")
            .columns
            .tolist()
        )