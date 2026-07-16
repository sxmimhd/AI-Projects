from pathlib import Path

import random

import pandas as pd

import matplotlib.pyplot as plt

from PIL import Image

from config import settings

from src.utils.logger import Logger


class DatasetAnalyzer:

    def __init__(self, dataset, dataset_type):

        self.dataset = dataset

        self.dataset_type = dataset_type


    def analyze(self):

        if self.dataset_type == "vision":

            self.analyze_images()

        elif self.dataset_type == "nlp":

            self.analyze_text()

    def analyze_images(self):

        class_counts = {}

        image_widths = []

        image_heights = []

        sample_images = []

        for class_folder in self.dataset:

            images = [

                image

                for image in class_folder.iterdir()

                if image.suffix.lower() in [
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".bmp",
                    ".webp"
                ]

            ]

            class_counts[class_folder.name] = len(images)

            if images:

                sample_images.append(random.choice(images))

            for image_path in images:

                try:

                    image = Image.open(image_path)

                    image_widths.append(image.width)

                    image_heights.append(image.height)

                except:

                    pass

        report = pd.DataFrame({

            "Metric": [

                "Classes",

                "Images",

                "Average Width",

                "Average Height"

            ],

            "Value": [

                len(class_counts),

                sum(class_counts.values()),

                round(sum(image_widths) / len(image_widths), 2),

                round(sum(image_heights) / len(image_heights), 2)

            ]

        })

        report.to_csv(

            settings.REPORTS_DIR / "dataset_analysis.csv",

            index=False

        )

        self.plot_class_distribution(class_counts)

        self.plot_sample_gallery(sample_images)

        Logger.success("Dataset analysis completed.")

    def plot_class_distribution(self, class_counts):

        plt.figure(figsize=(10,5))

        plt.bar(

            class_counts.keys(),

            class_counts.values()

        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(

            settings.FIGURES_DIR / "class_distribution.png",

            dpi=300

        )

        plt.close()

    def plot_sample_gallery(self, sample_images):

        plt.figure(figsize=(15,8))

        for index, image_path in enumerate(sample_images):

            plt.subplot(

                2,

                5,

                index + 1

            )

            image = Image.open(image_path)

            plt.imshow(image)

            plt.title(image_path.parent.name)

            plt.axis("off")

        plt.tight_layout()

        plt.savefig(

            settings.FIGURES_DIR / "sample_gallery.png",

            dpi=300

        )

        plt.close()

    def analyze_text(self):

        Logger.info(

            "Text analyzer will be implemented later."

        )