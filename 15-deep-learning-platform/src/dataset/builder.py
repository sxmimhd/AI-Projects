from pathlib import Path
from sklearn.model_selection import train_test_split
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from config import settings
from src.utils.logger import Logger
from torch.utils.data import DataLoader, Subset
import numpy as np

class DatasetBuilder:

    def __init__(

        self,

        dataset_path,

        transforms

    ):

        self.dataset_path = Path(dataset_path)

        self.transforms = transforms


    def build(self):

        train_dataset = ImageFolder(
            self.dataset_path,
            transform=self.transforms["train"]
        )

        evaluation_dataset = ImageFolder(
            self.dataset_path,
            transform=self.transforms["validation"]
        )

        indices = np.arange(len(train_dataset))

        train_indices, temp_indices = train_test_split(
            indices,
            test_size=0.30,
            random_state=42,
            stratify=train_dataset.targets
        )

        temp_targets = [train_dataset.targets[i] for i in temp_indices]

        validation_indices, test_indices = train_test_split(
            temp_indices,
            test_size=0.50,
            random_state=42,
            stratify=temp_targets
        )

        train_subset = Subset(
            train_dataset,
            train_indices
        )

        validation_subset = Subset(
            evaluation_dataset,
            validation_indices
        )

        test_subset = Subset(
            evaluation_dataset,
            test_indices
        )

        train_loader = DataLoader(
            train_subset,
            batch_size=settings.BATCH_SIZE,
            shuffle=True,
            num_workers=settings.NUM_WORKERS
        )

        validation_loader = DataLoader(
            validation_subset,
            batch_size=settings.BATCH_SIZE,
            shuffle=False,
            num_workers=settings.NUM_WORKERS
        )

        test_loader = DataLoader(
            test_subset,
            batch_size=settings.BATCH_SIZE,
            shuffle=False,
            num_workers=settings.NUM_WORKERS
        )

        Logger.success("Dataset split completed.")

        Logger.info(f"Training Samples : {len(train_subset)}")
        Logger.info(f"Validation Samples : {len(validation_subset)}")
        Logger.info(f"Testing Samples : {len(test_subset)}")

        return {

            "train": train_loader,
            "validation": validation_loader,
            "test": test_loader,

            "classes": train_dataset.classes,

            "transforms": self.transforms

        }