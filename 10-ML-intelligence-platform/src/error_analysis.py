import os

import pandas as pd

import plotly.express as px

from sklearn.pipeline import Pipeline

from config.constants import (
    REGRESSION,
    CLASSIFICATION
)

class ErrorAnalysis:

    def __init__(
        self,
        optimizer,
        feature_engineer,
        preprocessor,
        problem_type
    ):

        self.optimizer = optimizer
        self.engineer = feature_engineer
        self.preprocessor = preprocessor
        self.problem_type = problem_type

        self.error_df = pd.DataFrame()

    def regression_analysis(self):

        pipeline = Pipeline(
            [
                ("preprocessor", self.preprocessor),
                ("model", self.optimizer.best_model)
            ]
        )

        pipeline.fit(
            self.engineer.X_train,
            self.engineer.y_train
        )

        predictions = pipeline.predict(
            self.engineer.X_test
        )

        self.error_df = pd.DataFrame(
            {
                "Actual": self.engineer.y_test,
                "Predicted": predictions
            }
        )

        self.error_df["Absolute Error"] = (
            self.error_df["Actual"]
            -
            self.error_df["Predicted"]
        ).abs()

        self.error_df = self.error_df.sort_values(
            "Absolute Error",
            ascending=False
        )

    def classification_analysis(self):

        pipeline = Pipeline(
            [
                ("preprocessor", self.preprocessor),
                ("model", self.optimizer.best_model)
            ]
        )

        pipeline.fit(
            self.engineer.X_train,
            self.engineer.y_train
        )

        predictions = pipeline.predict(
            self.engineer.X_test
        )

        self.error_df = self.engineer.X_test.copy()

        self.error_df["Actual"] = self.engineer.y_test.values

        self.error_df["Predicted"] = predictions

        self.error_df["Correct"] = (
            self.error_df["Actual"]
            ==
            self.error_df["Predicted"]
        )

        self.error_df = self.error_df[
            self.error_df["Correct"] == False
        ]

    def analyze(self):

        if self.problem_type == REGRESSION:

            self.regression_analysis()

        else:

            self.classification_analysis()

    def charts(self):

        os.makedirs(
            "outputs/charts",
            exist_ok=True
        )

        if self.problem_type == REGRESSION:

            fig = px.scatter(
                self.error_df,
                x="Actual",
                y="Predicted",
                title="Actual vs Predicted"
            )

            fig.write_html(
                "outputs/charts/actual_vs_predicted.html"
            )

            fig.write_image(
                "outputs/charts/actual_vs_predicted.png"
            )

            fig = px.histogram(
                self.error_df,
                x="Absolute Error",
                title="Prediction Error Distribution"
            )

            fig.write_html(
                "outputs/charts/error_distribution.html"
            )

            fig.write_image(
                "outputs/charts/error_distribution.png"
            )

        else:

            counts = (
                self.error_df["Actual"]
                .value_counts()
                .reset_index()
            )

            counts.columns = [
                "Class",
                "Errors"
            ]

            fig = px.bar(
                counts,
                x="Class",
                y="Errors",
                title="Misclassified Samples"
            )

            fig.write_html(
                "outputs/charts/misclassified_samples.html"
            )

            fig.write_image(
                "outputs/charts/misclassified_samples.png"
            )

    def summary(self):

        print()

        print("=" * 60)

        print("ERROR ANALYSIS")

        print("=" * 60)

        print()

        print(
            self.error_df.head(20)
        )