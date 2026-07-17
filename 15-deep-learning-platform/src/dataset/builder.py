from pathlib import Path

from sklearn.model_selection import train_test_split

from torchvision.datasets import ImageFolder

from torch.utils.data import DataLoader

from config import settings

from src.utils.logger import Logger


class DatasetBuilder:

    def __init__(

        self,

        dataset_path,

        transforms

    ):

        self.dataset_path = Path(dataset_path)

        self.transforms = transforms


    def build(self):

        dataset = ImageFolder(

            self.dataset_path,

            transform=self.transforms["train"]

        )

        train_size = int(0.7 * len(dataset))

        validation_size = int(0.15 * len(dataset))

        test_size = len(dataset) - train_size - validation_size

        from torch.utils.data import random_split

        train_dataset, validation_dataset, test_dataset = random_split(

            dataset,

            [

                train_size,

                validation_size,

                test_size

            ]

        )

        validation_dataset.dataset.transform = self.transforms["validation"]

        test_dataset.dataset.transform = self.transforms["validation"]

        train_loader = DataLoader(

            train_dataset,

            batch_size=settings.BATCH_SIZE,

            shuffle=True,

            num_workers=settings.NUM_WORKERS

        )

        validation_loader = DataLoader(

            validation_dataset,

            batch_size=settings.BATCH_SIZE,

            shuffle=False,

            num_workers=settings.NUM_WORKERS

        )

        test_loader = DataLoader(

            test_dataset,

            batch_size=settings.BATCH_SIZE,

            shuffle=False,

            num_workers=settings.NUM_WORKERS

        )

        Logger.success("Dataset split completed.")

        Logger.info(f"Training Samples : {len(train_dataset)}")

        Logger.info(f"Validation Samples : {len(validation_dataset)}")

        Logger.info(f"Testing Samples : {len(test_dataset)}")

        return {

            "train": train_loader,

            "validation": validation_loader,

            "test": test_loader,

            "classes": dataset.classes

        }