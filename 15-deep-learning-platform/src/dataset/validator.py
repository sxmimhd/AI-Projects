from pathlib import Path

import pandas as pd
from PIL import Image

from src.utils.logger import Logger


class DatasetValidator:

    def __init__(self, dataset, dataset_type):

        self.dataset = dataset
        self.dataset_type = dataset_type

        self.report = {}


    def validate(self):

        if self.dataset_type == "vision":

            return self.validate_images()

        elif self.dataset_type == "nlp":

            return self.validate_text()

    # IMAGE DATASET

    def validate_images(self):

        total_images = 0
        corrupted_images = 0
        empty_classes = []

        class_distribution = {}

        for class_folder in self.dataset:

            image_count = 0

            for image_path in class_folder.glob("*"):

                if image_path.suffix.lower() not in [
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".bmp",
                    ".webp"
                ]:
                    continue

                image_count += 1
                total_images += 1

                try:

                    with Image.open(image_path) as image:

                        image.verify()

                except Exception:

                    corrupted_images += 1

            class_distribution[class_folder.name] = image_count

            if image_count == 0:

                empty_classes.append(class_folder.name)

        self.report = {

            "Dataset Type": "Vision",

            "Classes": len(class_distribution),

            "Total Images": total_images,

            "Corrupted Images": corrupted_images,

            "Empty Classes": empty_classes,

            "Class Distribution": class_distribution

        }

        Logger.success("Vision dataset validation completed.")

        return self.report

    # NLP DATASET

    def validate_text(self):

        missing_reviews = self.dataset["review_text"].isna().sum()

        duplicates = self.dataset.duplicated().sum()

        self.report = {

            "Dataset Type": "NLP",

            "Samples": len(self.dataset),

            "Missing Reviews": missing_reviews,

            "Duplicate Samples": duplicates

        }

        Logger.success("Text dataset validation completed.")

        return self.report