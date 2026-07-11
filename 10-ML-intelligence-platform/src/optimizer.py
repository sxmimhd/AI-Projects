import pandas as pd

from sklearn.pipeline import Pipeline

from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV
)

from config.constants import (
    REGRESSION,
    CLASSIFICATION
)

class Optimizer:

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

        self.best_estimators = {}

        
        self.best_model = None

        self.best_model_name = None

        self.best_score = float("-inf")

    def parameter_grids(self):

        if self.problem_type == REGRESSION:

            return {

                "Random Forest": {

                    "model__n_estimators":[100,200],

                    "model__max_depth":[None,10,20]

                },

                "Gradient Boosting":{

                    "model__n_estimators":[100,200],

                    "model__learning_rate":[0.05,0.1],

                    "model__max_depth":[3,5]

                }

            }

        else:

            return {

                "Random Forest":{

                    "model__n_estimators":[100,200],

                    "model__max_depth":[None,10,20]

                },

                "Gradient Boosting":{

                    "model__n_estimators":[100,200],

                    "model__learning_rate":[0.05,0.1]

                }

            }
        
    def grid_search(self):

        grids = self.parameter_grids()

        rows = []

        scoring = "r2"

        if self.problem_type == CLASSIFICATION:

            scoring = "roc_auc"

        for name, parameters in grids.items():

            pipeline = Pipeline(

                [

                    ("preprocessor", self.preprocessor),

                    ("model", self.models[name])

                ]

            )

            search = GridSearchCV(

                estimator=pipeline,

                param_grid=parameters,

                cv=5,

                scoring=scoring,

                n_jobs=-1

            )

            search.fit(

                self.engineer.X,

                self.engineer.y

            )

            self.best_estimators[name] = search.best_estimator_

            if search.best_score_ > self.best_score:

                self.best_score = search.best_score_

                self.best_model = search.best_estimator_

                self.best_model_name = name

            rows.append(

                {

                    "Model":name,

                    "Best Score":search.best_score_,

                    "Best Parameters":str(search.best_params_)

                }

            )

        self.results = pd.DataFrame(rows)

        return self.results
    
    def summary(self):

        print()

        print("=" * 60)

        print("GRID SEARCH")

        print("=" * 60)

        print()
        
        print(f"Best Model : {self.best_model_name}")
        print(

            self.results.sort_values(

                "Best Score",

                ascending=False

            )

        )