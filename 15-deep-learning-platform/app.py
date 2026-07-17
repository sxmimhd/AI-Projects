from src.utils.logger import Logger
from config import settings
from src.utils.helpers import create_output_directories
from src.dataset.loader import DatasetLoader
from src.dataset.validator import DatasetValidator
from src.dataset.analyzer import DatasetAnalyzer
from src.tasks.detector import TaskDetector
from src.models.model_selector import ModelSelector
from src.models.factory import ModelFactory
from src.preprocessing.image_preprocessor import ImagePreprocessor
from src.preprocessing.text_preprocessor import TextPreprocessor
from src.dataset.builder import DatasetBuilder
from src.models.summary import ModelSummary
from src.training.trainer import Trainer
from src.training.evaluator import Evaluator
from src.training.plots import TrainingPlots
from src.persistence.loader import ModelLoader
from src.prediction.predictor import Predictor
from src.persistence.saver import ModelSaver
from src.visualization.predictions import PredictionPlots
from src.explainability.gradcam import GradCAM
from src.preprocessing.tokenizer import Tokenizer
from src.dataset.text_builder import TextDatasetBuilder

def main():

    create_output_directories(settings)

    Logger.success("Deep Learning Platform Started")

    Logger.info(f"Device : {settings.DEVICE}")

    Logger.info("Waiting for user input...")

    loader = DatasetLoader(

        "data/reviews/dataset.csv"

    )

    dataset = loader.load()

    validator = DatasetValidator(

        dataset,

        loader.dataset_type

    )

    report = validator.validate()

    print()

    for key, value in report.items():

        print(f"{key} : {value}")

    analyzer = DatasetAnalyzer(

    dataset,

    loader.dataset_type

    )

    analyzer.analyze()

    detector = TaskDetector(

    loader.dataset_type

    )
    task = detector.detect()

    selector = ModelSelector(
    task["task"]
    )
    model_name = selector.select()

    if loader.dataset_type == "vision":
        preprocessor = ImagePreprocessor()
        pipeline = preprocessor.build()
        builder = DatasetBuilder(
            "data/reviews/dataset.csv",
            pipeline
        )
        dataloaders = builder.build()

    else:
        preprocessor = TextPreprocessor()
        clean_function = preprocessor.build()
        text_column = loader.text_column
        target_column = loader.target_column

        dataset = dataset.dropna(
            subset=[text_column, target_column]
        )

        dataset[text_column] = dataset[text_column].astype(str)

        dataset[text_column] = dataset[text_column].apply(
            clean_function
        )

        tokenizer = Tokenizer(
            max_length=settings.MAX_SEQUENCE_LENGTH
        )
        tokenizer.fit(
            dataset[text_column]
        )

        builder = TextDatasetBuilder(
            dataframe=dataset,
            tokenizer=tokenizer,
            text_column=text_column,
            target_column=target_column
            
        )

        dataset[target_column] = dataset[target_column].astype("category").cat.codes

        classes = dataset[target_column].nunique()
        if classes != 2:
            raise ValueError(
                "Current SentimentClassifier supports binary classification only."
            )
        
        dataloaders = builder.build()
        

    if loader.dataset_type == "vision":

        model = ModelFactory.create(
            model_name,
            num_classes=len(
                dataloaders["classes"]
            )
        )

    else:
        model = ModelFactory.create(
            model_name,
            vocabulary_size=
            tokenizer.vocabulary_size
        )

    ModelSummary.save(model)

    trainer = Trainer(
    model,
    dataloaders["train"],
    dataloaders["validation"]
    )
    history = trainer.train()
    TrainingPlots.history(history)

    config = {

        "model": model.__class__.__name__,
        "batch_size": settings.BATCH_SIZE,
        "learning_rate": settings.LEARNING_RATE,
        "epochs": settings.EPOCHS
    }

    if loader.dataset_type == "vision":
        config["image_size"] = settings.IMAGE_SIZE
        config["classes"] = len(
            dataloaders["classes"]
        )
    else:
        config["vocabulary_size"] = tokenizer.vocabulary_size
        config["sequence_length"] = settings.MAX_SEQUENCE_LENGTH


    if loader.dataset_type == "vision":
        ModelSaver.save(
            model,
            dataloaders["classes"],
            config
        )
    else:
        ModelSaver.save(
            model,
            tokenizer.vocabulary,
            config
        )

    package = ModelLoader.load(model)
    model = package["model"]


    if loader.dataset_type == "vision":
        evaluator = Evaluator(
            model,
            dataloaders["test"],
            dataloaders["classes"]
        )
    else:
        evaluator = Evaluator(
            model,
            dataloaders["test"]
        )
    results = evaluator.evaluate()


    if loader.dataset_type == "vision":
        TrainingPlots.confusion_matrix(
            results["confusion_matrix"],
            dataloaders["classes"]
        )

        predictor = Predictor(
            model,
            dataloaders["transforms"]["validation"],
            dataloaders["classes"]
        )
        predictor.predict(
            "data/games/Minecraft/image_24.png"
        )
        PredictionPlots.confidence()


if __name__ == "__main__":

    main()