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


def main():

    create_output_directories(settings)

    Logger.success("Deep Learning Platform Started")

    Logger.info(f"Device : {settings.DEVICE}")

    Logger.info("Waiting for user input...")

    loader = DatasetLoader(

        "data/games"

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
    else:
        preprocessor = TextPreprocessor()
    pipeline = preprocessor.build()

    if loader.dataset_type == "vision":
        builder = DatasetBuilder(
            "data/games",
            pipeline
        )
        dataloaders = builder.build()

    model = ModelFactory.create(
        model_name,
        len(dataloaders["classes"])
    )

    ModelSummary.save(model)

    trainer = Trainer(
    model,
    dataloaders["train"],
    dataloaders["validation"]
    )
    trainer.train()




if __name__ == "__main__":

    main()