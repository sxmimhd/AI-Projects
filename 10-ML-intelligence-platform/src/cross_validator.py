import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.model_selection import cross_val_score

from config.constants import (
    REGRESSION,
    CLASSIFICATION
)

class CrossValidator:

    def __init__(

        self,

        models,

        preprocessor,

        feature_engineer,

        problem_type

    ):

        self.models = models

        self.preprocessor = preprocessor

        self.engineer = feature_engineer

        self.problem_type = problem_type

        self.results = pd.DataFrame()

    def evaluate(self):

        if self.problem_type == REGRESSION:

            scoring = "r2"

        else:

            scoring = "roc_auc"

        rows = []

        for name, model in self.models.items():

            pipeline = Pipeline(

                [

                    ("preprocessor", self.preprocessor),

                    ("model", model)

                ]

            )

            scores = cross_val_score(

                pipeline,

                self.engineer.X,

                self.engineer.y,

                cv=5,

                scoring=scoring,

                n_jobs=-1

            )

            rows.append(

                {

                    "Model": name,

                    "Mean Score": scores.mean(),

                    "Std": scores.std()

                }

            )

        self.results = pd.DataFrame(rows)

        return self.results
    
    def summary(self):

        print()

        print("=" * 60)

        print("CROSS VALIDATION")

        print("=" * 60)

        print()

        print(

            self.results.sort_values(

                "Mean Score",

                ascending=False

            )

        )