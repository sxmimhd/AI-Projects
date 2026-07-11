import numpy as np
import pandas as pd


class DatasetValidator:
    
    def __init__(self, dataset: pd.DataFrame):

        self.dataset = dataset

        self.missing_values = None
        self.duplicate_rows = 0
        self.empty_columns = []
        self.constant_columns = []
        self.invalid_numeric_columns = []
        self.high_cardinality_columns = []

        self.quality_score = 100

    def validate(self):

        self._check_missing_values()

        self._check_duplicates()

        self._check_empty_columns()

        self._check_constant_columns()

        self._check_invalid_numeric()

        self._check_high_cardinality()

        self._calculate_quality_score()

    def _check_missing_values(self):

        self.missing_values = self.dataset.isnull().sum()
        
    def _check_duplicates(self):

        self.duplicate_rows = self.dataset.duplicated().sum()

    def _check_empty_columns(self):

        self.empty_columns = []

        for column in self.dataset.columns:

            if self.dataset[column].isnull().all():

                self.empty_columns.append(column)

    def _check_constant_columns(self):

        self.constant_columns = []

        for column in self.dataset.columns:

            if self.dataset[column].nunique(dropna=False) == 1:

                self.constant_columns.append(column)

    def _check_invalid_numeric(self):

        self.invalid_numeric_columns = []

        numeric = self.dataset.select_dtypes(include="number")

        for column in numeric.columns:

            if np.isinf(numeric[column]).any():

                self.invalid_numeric_columns.append(column)

    def _check_high_cardinality(self):

        self.high_cardinality_columns = []

        categorical = self.dataset.select_dtypes(exclude="number")

        for column in categorical.columns:

            if self.dataset[column].nunique() > 100:

                self.high_cardinality_columns.append(column)

    def _calculate_quality_score(self):

        score = 100

        score -= min(
            self.missing_values.sum() / len(self.dataset),
            30
        )

        score -= min(self.duplicate_rows, 20)

        score -= len(self.empty_columns) * 5

        score -= len(self.constant_columns) * 5

        score -= len(self.invalid_numeric_columns) * 5

        score -= len(self.high_cardinality_columns) * 2

        self.quality_score = max(round(score, 2), 0)

    @property
    def quality_label(self):

        if self.quality_score >= 90:
            return "Excellent"

        elif self.quality_score >= 75:
            return "Good"

        elif self.quality_score >= 60:
            return "Average"

        return "Poor"