import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

class DatasetPreprocessor:

    def __init__(self, dataset: pd.DataFrame):

        self.dataset = dataset

        self.numeric_features = []

        self.categorical_features = []

        self.preprocessor = None

    def build(self):

        self._detect_features()

        self._create_pipeline()

        return self.preprocessor
    
    def _detect_features(self):

        self.numeric_features = (
            self.dataset
            .select_dtypes(include="number")
            .columns
            .tolist()
        )

        self.categorical_features = (
            self.dataset
            .select_dtypes(exclude="number")
            .columns
            .tolist()
        )
    
    def _create_pipeline(self):

        numeric_pipeline = Pipeline(

            steps=[

                (
                    "imputer",
                    SimpleImputer(strategy="median")
                ),

                (
                    "scaler",
                    StandardScaler()
                )

            ]

        )

        categorical_pipeline = Pipeline(

            steps=[

                (
                    "imputer",
                    SimpleImputer(strategy="most_frequent")
                ),

                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )

            ]

        )

        self.preprocessor = ColumnTransformer(

            transformers=[

                (
                    "num",
                    numeric_pipeline,
                    self.numeric_features
                ),

                (
                    "cat",
                    categorical_pipeline,
                    self.categorical_features
                )

            ]

        )

        