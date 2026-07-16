from src.utils.logger import Logger
from config import settings
from src.utils.helpers import create_output_directories
from src.dataset.loader import DatasetLoader
from src.dataset.validator import DatasetValidator
from src.dataset.analyzer import DatasetAnalyzer
from src.tasks.detector import TaskDetector
from src.models.model_selector import ModelSelector

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
    model = selector.select()


if __name__ == "__main__":

    main()