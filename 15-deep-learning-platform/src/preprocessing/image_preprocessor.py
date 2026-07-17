from torchvision import transforms

from config import settings

from src.utils.logger import Logger


class ImagePreprocessor:

    def __init__(self):

        self.train_transform = None
        self.validation_transform = None

    def build(self):

        self.train_transform = transforms.Compose([

            transforms.Resize(
                (settings.IMAGE_SIZE, settings.IMAGE_SIZE)
            ),

            transforms.RandomHorizontalFlip(),

            transforms.RandomRotation(10),

            transforms.ColorJitter(
                brightness=0.2,
                contrast=0.2,
                saturation=0.2
            ),

            transforms.ToTensor(),

            transforms.Normalize(

                mean=[0.485, 0.456, 0.406],

                std=[0.229, 0.224, 0.225]

            )

        ])

        self.validation_transform = transforms.Compose([

            transforms.Resize(
                (settings.IMAGE_SIZE, settings.IMAGE_SIZE)
            ),

            transforms.ToTensor(),

            transforms.Normalize(

                mean=[0.485, 0.456, 0.406],

                std=[0.229, 0.224, 0.225]

            )

        ])

        Logger.success(
            "Vision preprocessing pipeline created."
        )

        return {

            "train": self.train_transform,

            "validation": self.validation_transform

        }