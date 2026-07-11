import pandas as pd

from config.constants import (
    CLASSIFICATION,
    REGRESSION
)

class ProblemDetector:

    def __init__(self, dataset: pd.DataFrame):

        self.dataset = dataset

        self.target = None

        self.problem_type = None

    def detect(self, target_column: str):

        self.target = target_column

        column = self.dataset[target_column]

        self.problem_type = self._infer_problem(column)

        return self.problem_type
    
    def _infer_problem(self, column):

        if column.dtype == object:

            return CLASSIFICATION

        unique = column.nunique()

        if unique <= 20:

            return CLASSIFICATION

        return REGRESSION
    
    @property
    def is_classification(self):

        return self.problem_type == CLASSIFICATION
    
    @property
    def is_regression(self):

        return self.problem_type == REGRESSION