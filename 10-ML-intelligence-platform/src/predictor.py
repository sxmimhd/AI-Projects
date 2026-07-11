import joblib
import pandas as pd

from sklearn.pipeline import Pipeline

class Predictor:

    def __init__(

        self,

        feature_engineer

    ):

        self.engineer = feature_engineer

        self.model = joblib.load(
            "models/model.pkl"
        )

        self.preprocessor = joblib.load(
            "models/preprocessor.pkl"
        )

    def demo_prediction(self):

        sample = self.engineer.X_test.iloc[[0]]

        pipeline = Pipeline(

            [

                ("preprocessor", self.preprocessor),

                ("model", self.model)

            ]

        )

        prediction = pipeline.predict(sample)

        print()

        print("=" * 60)

        print("PREDICTION MODE")

        print("=" * 60)

        print()

        print("Sample")

        print(sample)

        print()

        print("Prediction")

        print(prediction)