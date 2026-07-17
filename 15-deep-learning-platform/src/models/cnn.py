import torch.nn as nn

from src.utils.logger import Logger


class CNNModel:

    def __init__(

        self,

        num_classes

    ):

        self.num_classes = num_classes

    def build(self):

        model = nn.Sequential(

            nn.Conv2d(
                3,
                32,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            nn.MaxPool2d(2),

            nn.Conv2d(
                32,
                64,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            nn.MaxPool2d(2),

            nn.Conv2d(
                64,
                128,
                kernel_size=3,
                padding=1
            ),

            nn.ReLU(),

            nn.MaxPool2d(2),

            nn.Flatten(),

            nn.Linear(
                128 * 28 * 28,
                512
            ),

            nn.ReLU(),

            nn.Dropout(0.5),

            nn.Linear(
                512,
                self.num_classes
            )

        )

        Logger.success(
            "Custom CNN model created."
        )

        return model