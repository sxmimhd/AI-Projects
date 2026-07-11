from src.loader import DatasetLoader
from src.validator import DatasetValidator
from src.profiler import DatasetProfiler
from src.preprocessing import DatasetPreprocessor
from src.problem_detector import ProblemDetector
from src.feature_engineering import FeatureEngineer
from src.model_selector import ModelSelector
from src.cross_validator import CrossValidator
from src.optimizer import Optimizer
from src.feature_selector import FeatureSelector
from src.explainability import Explainability
from src.error_analysis import ErrorAnalysis
from src.persistence import ModelPersistence
from src.predictor import Predictor
from src.exporter import Exporter

def main():

    loader = DatasetLoader()
    loader.load_csv("data/Games_Sales.csv")

    print("=" * 50)
    print("ML Intelligence Platform")
    print("=" * 50)
    print()
    print(f"Dataset : {loader.file_name}")
    print(f"Rows    : {loader.rows:,}")
    print(f"Columns : {loader.columns}")
    print(f"Memory  : {loader.memory_usage:.2f} MB")
    print()
    print("Numeric Columns")
    print(loader.numeric_columns)
    print()
    print("Categorical Columns")
    print(loader.categorical_columns)

    validator = DatasetValidator(loader.dataset)
    validator.validate()

    print("=" * 60)
    print("DATASET VALIDATION")
    print("=" * 60)

    print()

    print(
    f"Quality Score : "
    f"{validator.quality_score}/100 "
    f"({validator.quality_label})"
    )

    print(f"Duplicate Rows : {validator.duplicate_rows}")
    print()
    print("Empty Columns")
    print(validator.empty_columns)
    print()
    print("Constant Columns")
    print(validator.constant_columns)
    print()
    print("Invalid Numeric Columns")
    print(validator.invalid_numeric_columns)
    print()
    print("High Cardinality")
    print(validator.high_cardinality_columns)
    print()

    print("Missing Values")
    missing = validator.missing_values[
    validator.missing_values > 0
    ]
    print(missing)

    profiler = DatasetProfiler(loader.dataset)
    profiler.profile()

    print("=" * 60)
    print("DATASET PROFILING")
    print("=" * 60)
    print()
    print("Statistics")
    print(profiler.statistics)
    print()
    print("Skewness")
    print(profiler.skewness)
    print()
    print("Kurtosis")
    print(profiler.kurtosis)
    print()
    print("Outliers")
    print(profiler.outliers)
    print()
    print("Correlation Matrix")
    print(profiler.correlation)


    detector = ProblemDetector(loader.dataset)

    print("=" * 60)
    print("TARGET SELECTION")
    print("=" * 60)
    print()

    for i, column in enumerate(loader.dataset.columns, start=1):
        print(f"{i}. {column}")

    choice = int(input("\nChoose target column number: "))
    target = loader.dataset.columns[choice - 1]

    problem = detector.detect(target)

    print()
    print("=" * 60)
    print("PROBLEM DETECTION")
    print("=" * 60)

    print()

    print(f"Target Column : {target}")

    print(f"Problem Type  : {problem}")


    engineer = FeatureEngineer(
    dataset=loader.dataset,
    target=target,
    problem_type=problem
    )

    engineer.prepare()
    engineer.summary()

    preprocessor = DatasetPreprocessor(engineer.X)
    pipeline = preprocessor.build()

    print("=" * 60)
    print("PREPROCESSING")
    print("=" * 60)

    print()
    print("Numeric Features")
    for feature in preprocessor.numeric_features:

        print(f"• {feature}")
    print()
    print("Categorical Features")
    for feature in preprocessor.categorical_features:

        print(f"• {feature}")
    print()
    print("Pipeline Created Successfully")


    selector = ModelSelector(
    preprocessor=pipeline,
    feature_engineer=engineer,
    problem_type=problem
    )

    selector.train_models()
    selector.summary()

    cross_validator = CrossValidator(
    models=selector.models,
    preprocessor=pipeline,
    feature_engineer=engineer,
    problem_type=problem
    )
    cross_validator.evaluate()
    cross_validator.results.to_csv(

        "outputs/reports/cross_validation_results.csv",

        index=False

    )
    cross_validator.summary()


    optimizer = Optimizer(
    models=selector.models,
    preprocessor=pipeline,
    feature_engineer=engineer,
    problem_type=problem
    )
    optimizer.grid_search()
    optimizer.summary()
    optimizer.results.to_csv(
        "outputs/reports/grid_search_results.csv",
        index=False
    )


    feature_selector = FeatureSelector(
    preprocessor=pipeline,
    feature_engineer=engineer,
    problem_type=problem
    )
    feature_selector.prepare()
    feature_selector.select_k_best()
    feature_selector.rfe()
    feature_selector.summary()

    feature_selector.selectkbest_results.to_csv(
    "outputs/reports/select_k_best.csv",
    index=False
    )
    feature_selector.rfe_results.to_csv(
        "outputs/reports/rfe_results.csv",
        index=False
    )

    explainer = Explainability(
    optimizer=optimizer,
    feature_engineer=engineer,
    preprocessor=pipeline,
    problem_type=problem
    )
    explainer.feature_importances()
    explainer.permutation()
    explainer.summary()
    explainer.business_summary()
    explainer.feature_importance.to_csv(
    "outputs/reports/feature_importance.csv",
    index=False
    )
    explainer.permutation_importance.to_csv(
        "outputs/reports/permutation_importance.csv",
        index=False
    )

    error_analysis = ErrorAnalysis(
    optimizer=optimizer,
    feature_engineer=engineer,
    preprocessor=pipeline,
    problem_type=problem
    )
    error_analysis.analyze()
    error_analysis.summary()
    error_analysis.charts()
    error_analysis.error_df.to_csv(
        "outputs/reports/error_analysis.csv",
        index=False
    )

    persistence = ModelPersistence(
    optimizer=optimizer,
    preprocessor=pipeline
    )
    persistence.save()

    predictor = Predictor(engineer)
    predictor.demo_prediction()

    exporter = Exporter()
    exporter.export_summary(
        validator,
        selector,
        cross_validator,
        optimizer
    )

if __name__ == "__main__":
    main()