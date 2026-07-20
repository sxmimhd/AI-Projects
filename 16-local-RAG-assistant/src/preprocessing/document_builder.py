import ast
import pandas as pd

from src.utils.logger import Logger
from src.core.document import Document

class DocumentBuilder:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.logger = Logger.get_logger()

    def build(self) -> list[dict]:
        documents = []

        for _, row in self.df.iterrows():
            documents.append(
                Document(
                    game_id=row["appid"],
                    title=row["name"],
                    document=self.build_document(row),
                    metadata={
                        "genres": self.parse_list(row["genres"]),
                        "tags": self.parse_tags(row["tags"]),
                        "developers": self.parse_list(row["developers"]),
                        "publishers": self.parse_list(row["publishers"]),
                        "price": row["price"],
                        "release_date": row["release_date"],
                    },
                )
            )

        self.logger.info(
            f"Built {len(documents):,} knowledge documents."
        )

        return documents

    @staticmethod
    def build_document(row: pd.Series) -> str:
        sections = [
            row["name"],
            ", ".join(DocumentBuilder.parse_list(row["genres"])),
            row["detailed_description"],
        ]

        return "\n\n".join(
            section.strip()
            for section in sections
            if isinstance(section, str) and section.strip()
        )

    @staticmethod
    def parse_list(value) -> list[str]:
        if pd.isna(value):
            return []

        if isinstance(value, list):
            return value

        try:
            parsed = ast.literal_eval(str(value))
            return parsed if isinstance(parsed, list) else []
        except Exception:
            return []

    @staticmethod
    def parse_tags(value) -> list[str]:
        if pd.isna(value):
            return []

        if isinstance(value, dict):
            return list(value.keys())

        try:
            parsed = ast.literal_eval(str(value))

            if isinstance(parsed, dict):
                return list(parsed.keys())

            return []

        except Exception:
            return []