from pathlib import Path

import pandas as pd

from src.utils.logger import Logger


class DatasetLoader:

    def __init__(self, dataset_path):

        self.dataset_path = Path(dataset_path)

        self.dataset = None

        self.dataset_type = None


    def load(self):

        if not self.dataset_path.exists():

            raise FileNotFoundError(
                f"{self.dataset_path} does not exist."
            )

        if self.dataset_path.is_dir():

            self.dataset_type = "vision"

            Logger.success("Image dataset detected.")

            return self.load_image_dataset()

        elif self.dataset_path.suffix.lower() == ".csv":

            self.dataset_type = "nlp"

            Logger.success("CSV dataset detected.")

            return self.load_text_dataset()

        else:

            raise ValueError("Unsupported dataset format.")


    def load_image_dataset(self):

        classes = [

            folder

            for folder in self.dataset_path.iterdir()

            if folder.is_dir()

        ]

        Logger.info(f"Classes Found : {len(classes)}")

        Logger.info(

            f"Class Names : {[folder.name for folder in classes]}"

        )

        self.dataset = classes

        return classes


    def load_text_dataset(self):

        df = pd.read_csv(self.dataset_path)

        Logger.info(f"Dataset Shape : {df.shape}")

        self.dataset = df

        return df