import torch.nn as nn

from torchvision.models import (
    resnet18,
    ResNet18_Weights
)

from src.utils.logger import Logger


class TransferLearningModel:

    def __init__(

        self,

        num_classes,

        freeze_backbone=True

    ):

        self.num_classes = num_classes

        self.freeze_backbone = freeze_backbone


    def build(self):

        model = resnet18(

            weights=ResNet18_Weights.DEFAULT

        )

        if self.freeze_backbone:

            for parameter in model.parameters():

                parameter.requires_grad = False

        in_features = model.fc.in_features

        model.fc = nn.Sequential(

            nn.Dropout(0.4),

            nn.Linear(

                in_features,

                self.num_classes

            )

        )

        Logger.success(

            "Transfer Learning model created."

        )

        return model