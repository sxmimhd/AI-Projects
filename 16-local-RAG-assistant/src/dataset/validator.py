import pandas as pd

from src.utils.logger import Logger


class DatasetValidator:

    REQUIRED_COLUMNS = [
        "appid",
        "name",
        "detailed_description",
        "genres",
        "tags",
    ]

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.logger = Logger.get_logger()

    def validate(self) -> dict:
        report = {
            "valid": True,
            "missing_columns": self.check_required_columns(),
            "duplicate_appids": self.check_duplicate_appids(),
            "missing_titles": self.check_missing_titles(),
            "missing_descriptions": self.check_missing_descriptions(),
            "empty_descriptions": self.check_empty_descriptions(),
            "total_games": len(self.df),
        }

        report["valid"] = (
            len(report["missing_columns"]) == 0
            and report["duplicate_appids"] == 0
        )

        self.logger.info("Dataset validation completed.")

        return report

    def check_required_columns(self) -> list[str]:
        return [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in self.df.columns
        ]

    def check_duplicate_appids(self) -> int:
        if "appid" not in self.df.columns:
            return 0

        return int(self.df["appid"].duplicated().sum())

    def check_missing_titles(self) -> int:
        if "name" not in self.df.columns:
            return 0

        return int(self.df["name"].isna().sum())

    def check_missing_descriptions(self) -> int:
        if "detailed_description" not in self.df.columns:
            return 0

        return int(self.df["detailed_description"].isna().sum())

    def check_empty_descriptions(self) -> int:
        if "detailed_description" not in self.df.columns:
            return 0

        descriptions = (
            self.df["detailed_description"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        return int((descriptions == "").sum())

    def summary(self) -> dict:
        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "memory_mb": round(
                self.df.memory_usage(deep=True).sum() / (1024 ** 2),
                2
            ),
            "duplicates": int(self.df.duplicated().sum()),
        }