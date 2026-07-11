import pandas as pd

from sklearn.model_selection import train_test_split

from config.constants import (
    CLASSIFICATION,
    REGRESSION
)

class FeatureEngineer:

    def __init__(self, dataset, target, problem_type):

        self.dataset = dataset.copy()

        self.target = target

        self.problem_type = problem_type

        self.X = None
        self.y = None

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.numeric_features = None
        self.categorical_features = None

    def prepare(self):

        self._split_features_target()

        self._remove_identifier_columns()

        self._detect_feature_types()

        self._train_test_split()
    
    def _split_features_target(self):

        self.X = self.dataset.drop(columns=self.target)

        self.y = self.dataset[self.target]

    def _remove_identifier_columns(self):

        id_columns = []

        for column in self.X.columns:

            lower = column.lower()

            if (
                lower.endswith("id")
                or lower == "appid"
                or lower == "customerid"
            ):

                id_columns.append(column)

        self.X.drop(columns=id_columns,
                    inplace=True,
                    errors="ignore")
        
    def _detect_feature_types(self):

        self.numeric_features = self.X.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        self.categorical_features = self.X.select_dtypes(
            include=["object", "bool"]
        ).columns.tolist()

    def _train_test_split(self):

        if self.problem_type == CLASSIFICATION:

            (
                self.X_train,
                self.X_test,
                self.y_train,
                self.y_test
            ) = train_test_split(

                self.X,
                self.y,

                test_size=0.20,

                random_state=42,

                stratify=self.y
            )

        else:

            (
                self.X_train,
                self.X_test,
                self.y_train,
                self.y_test
            ) = train_test_split(

                self.X,
                self.y,

                test_size=0.20,

                random_state=42
            )

    def summary(self):

        print("=" * 60)

        print("FEATURE ENGINEERING")

        print("=" * 60)

        print()

        print("Training Shape :", self.X_train.shape)

        print("Testing Shape  :", self.X_test.shape)

        print()

        print("Numeric Features")

        print(self.numeric_features)

        print()

        print("Categorical Features")

        print(self.categorical_features)