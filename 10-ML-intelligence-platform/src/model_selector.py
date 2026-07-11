import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression
)

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,

    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from math import sqrt

from config.constants import (
    REGRESSION,
    CLASSIFICATION
)

class ModelSelector:

    def __init__(

        self,

        preprocessor,

        feature_engineer,

        problem_type

    ):

        self.preprocessor = preprocessor

        self.engineer = feature_engineer

        self.problem_type = problem_type

        self.models = {}

        self.results = pd.DataFrame()

    def train_models(self):

        if self.problem_type == REGRESSION:

            self._train_regression()

        else:

            self._train_classification()

        return self.results
    
    def _train_regression(self):

        self.models = {

            "Linear Regression":

                LinearRegression(),

            "Random Forest":

                RandomForestRegressor(
                    random_state=42
                ),

            "Gradient Boosting":

                GradientBoostingRegressor(
                    random_state=42
                )

        }

        rows = []

        for name, model in self.models.items():

            pipeline = Pipeline(

                [

                    ("preprocessor",
                    self.preprocessor),

                    ("model",
                    model)

                ]

            )

            pipeline.fit(

                self.engineer.X_train,

                self.engineer.y_train

            )

            predictions = pipeline.predict(

                self.engineer.X_test

            )

            rows.append(

                {

                    "Model": name,

                    "MAE":

                        mean_absolute_error(

                            self.engineer.y_test,

                            predictions

                        ),

                    "RMSE":

                        sqrt(

                            mean_squared_error(

                                self.engineer.y_test,

                                predictions

                            )

                        ),

                    "R²":

                        r2_score(

                            self.engineer.y_test,

                            predictions

                        )

                }

            )

        self.results = pd.DataFrame(rows)

    def _train_classification(self):

        self.models = {

            "Logistic Regression":

                LogisticRegression(
                    max_iter=1000
                ),

            "Decision Tree":

                DecisionTreeClassifier(
                    random_state=42
                ),

            "Random Forest":

                RandomForestClassifier(
                    random_state=42
                ),

            "Gradient Boosting":

                GradientBoostingClassifier(
                    random_state=42
                )

        }

        rows = []

        for name, model in self.models.items():

            pipeline = Pipeline(

                [

                    ("preprocessor",
                    self.preprocessor),

                    ("model",
                    model)

                ]

            )

            pipeline.fit(

                self.engineer.X_train,

                self.engineer.y_train

            )

            predictions = pipeline.predict(

                self.engineer.X_test
            )

            probabilities = pipeline.predict_proba(

                self.engineer.X_test

            )[:,1]

            rows.append(

                {

                    "Model": name,

                    "Accuracy":

                        accuracy_score(

                            self.engineer.y_test,

                            predictions

                        ),

                    "Precision":

                        precision_score(

                            self.engineer.y_test,

                            predictions,

                            zero_division=0

                        ),

                    "Recall":

                        recall_score(

                            self.engineer.y_test,

                            predictions

                        ),

                    "F1":

                        f1_score(

                            self.engineer.y_test,

                            predictions

                        ),

                    "ROC AUC":

                        roc_auc_score(

                            self.engineer.y_test,

                            probabilities

                        )

                }

            )

        self.results = pd.DataFrame(rows)

    def summary(self):

        print()

        print("=" * 60)

        print("MODEL COMPARISON")

        print("=" * 60)

        print()

        print(

            self.results.sort_values(

                by=self.results.columns[-1],

                ascending=False

            )

        )

    