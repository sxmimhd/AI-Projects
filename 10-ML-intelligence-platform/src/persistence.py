import os
import joblib

class ModelPersistence:

    def __init__(
        self,
        optimizer,
        preprocessor,
        feature_selector=None
    ):

        self.optimizer = optimizer
        self.preprocessor = preprocessor
        self.feature_selector = feature_selector

    def save(self):

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            self.optimizer.best_model,
            "models/model.pkl"
        )

        joblib.dump(
            self.preprocessor,
            "models/preprocessor.pkl"
        )

        if self.feature_selector is not None:

            joblib.dump(
                self.feature_selector,
                "models/feature_selector.pkl"
            )

        print()

        print("=" * 60)
        print("MODEL PERSISTENCE")
        print("=" * 60)

        print()

        print("✓ model.pkl")
        print("✓ preprocessor.pkl")

        if self.feature_selector is not None:

            print("✓ feature_selector.pkl")