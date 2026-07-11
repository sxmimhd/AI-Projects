import pandas as pd

from sklearn.feature_selection import (

    SelectKBest,

    mutual_info_regression,

    mutual_info_classif,

    RFE

)

from sklearn.linear_model import (

    LinearRegression,

    LogisticRegression

)

from config.constants import (

    REGRESSION,

    CLASSIFICATION

)

class FeatureSelector:

    def __init__(

        self,

        preprocessor,

        feature_engineer,

        problem_type

    ):

        self.preprocessor = preprocessor

        self.engineer = feature_engineer

        self.problem_type = problem_type

        self.transformed = None

        self.feature_names = None

        self.selectkbest_results = pd.DataFrame()

        self.rfe_results = pd.DataFrame()

    def prepare(self):

        self.transformed = self.preprocessor.fit_transform(

            self.engineer.X

        )

        self.feature_names = self.preprocessor.get_feature_names_out()

    def select_k_best(self, k=20):

        if self.problem_type == REGRESSION:

            selector = SelectKBest(

                score_func=mutual_info_regression,

                k=k

            )

        else:

            selector = SelectKBest(

                score_func=mutual_info_classif,

                k=k

            )

        selector.fit(

            self.transformed,

            self.engineer.y

        )

        self.selectkbest_results = pd.DataFrame(

            {

                "Feature":self.feature_names,

                "Score":selector.scores_

            }

        ).sort_values(

            "Score",

            ascending=False

        )

        return self.selectkbest_results
    
    def rfe(self, n_features=20):

        if self.problem_type == REGRESSION:

            estimator = LinearRegression()

        else:

            estimator = LogisticRegression(

                max_iter=1000

            )

        selector = RFE(

            estimator,

            n_features_to_select=n_features

        )

        selector.fit(

            self.transformed,

            self.engineer.y

        )

        self.rfe_results = pd.DataFrame(

            {

                "Feature":self.feature_names,

                "Selected":selector.support_,

                "Ranking":selector.ranking_

            }

        ).sort_values(

            "Ranking"

        )

        return self.rfe_results
    
    def summary(self):

        print()

        print("=" * 60)

        print("FEATURE SELECTION")

        print("=" * 60)

        print()

        print("Top SelectKBest Features")

        print()

        print(

            self.selectkbest_results.head(20)

        )

        print()

        print("Top RFE Features")

        print()

        print(

            self.rfe_results.head(20)

        )

    