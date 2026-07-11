import pandas as pd

from sklearn.inspection import permutation_importance

from config.constants import (
    REGRESSION,
    CLASSIFICATION
)

class Explainability:

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

        self.feature_importance = pd.DataFrame()

        self.permutation_importance = pd.DataFrame()

    def get_best_model(self):

        scores = self.optimizer.results.sort_values(

            "Best Score",

            ascending=False

        )

        best_name = scores.iloc[0]["Model"]

        model = self.optimizer.best_estimators[best_name]

        return best_name, model
    
    def feature_importances(self):

        name, model = self.get_best_model()

        model.fit(

            self.engineer.X,

            self.engineer.y

        )

        estimator = model.named_steps["model"]

        if not hasattr(estimator, "feature_importances_"):

            print()

            print(f"{name} does not provide built-in feature importance.")

            return

        names = model.named_steps[

            "preprocessor"

        ].get_feature_names_out()

        self.feature_importance = pd.DataFrame(

            {

                "Feature": names,

                "Importance": estimator.feature_importances_

            }

        ).sort_values(

            "Importance",

            ascending=False

        )

        return self.feature_importance
    
    def permutation(self):

        name, model = self.get_best_model()

        model.fit(

            self.engineer.X,

            self.engineer.y

        )

        result = permutation_importance(

            model,

            self.engineer.X,

            self.engineer.y,

            n_repeats=10,

            random_state=42,

            n_jobs=-1

        )

        self.permutation_importance = pd.DataFrame(

            {

                "Feature": self.engineer.X.columns,

                "Importance": result.importances_mean

            }

        ).sort_values(

            "Importance",

            ascending=False

        )

        return self.permutation_importance
    
    def business_summary(self):

        print()

        print("=" * 60)

        print("BUSINESS INSIGHTS")

        print("=" * 60)

        print()

        top = self.permutation_importance.head(5)

        for _, row in top.iterrows():

            print(

                f"• {row['Feature']} has a strong influence "

                f"({row['Importance']:.4f}) on predictions."

            )

    def summary(self):

        print()

        print("=" * 60)

        print("MODEL EXPLAINABILITY")

        print("=" * 60)

        print()

        if not self.feature_importance.empty:

            print(self.feature_importance.head(15))

            print()

        print(self.permutation_importance.head(15))