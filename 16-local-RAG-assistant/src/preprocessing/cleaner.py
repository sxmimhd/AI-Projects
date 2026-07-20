import html
import re

import pandas as pd

from src.utils.logger import Logger


class TextCleaner:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()
        self.logger = Logger.get_logger()

    def clean(self) -> pd.DataFrame:
        initial_rows = len(self.df)

        self.df = self.df.drop_duplicates(subset="appid")

        self.df = self.df.dropna(subset=["name", "detailed_description"])

        self.df["detailed_description"] = (
            self.df["detailed_description"]
            .astype(str)
            .apply(self.clean_text)
        )

        self.df = self.df[
            self.df["detailed_description"].str.strip() != ""
        ]

        removed_rows = initial_rows - len(self.df)

        self.logger.info(
            f"Text cleaning completed. Removed {removed_rows:,} invalid games."
        )

        return self.df.reset_index(drop=True)

    @staticmethod
    def clean_text(text: str) -> str:
        text = html.unescape(text)

        text = re.sub(r"<[^>]+>", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()