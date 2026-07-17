import torch.nn as nn

from torchvision.models import (
    resnet18,
    ResNet18_Weights
)

from src.utils.logger import Logger


class TransferLearningNetwork(nn.Module):

    def __init__(

        self,

        num_classes,

        freeze_backbone=True

    ):

        super().__init__()

        self.backbone = resnet18(
            weights=ResNet18_Weights.DEFAULT
        )

        if freeze_backbone:

            for parameter in self.backbone.parameters():
                parameter.requires_grad = False

        in_features = self.backbone.fc.in_features

        self.backbone.fc = nn.Sequential(

            nn.Dropout(0.4),

            nn.Linear(
                in_features,
                num_classes
            )

        )

    def forward(self, x):

        return self.backbone(x)


class TransferLearningModel:

    def __init__(

        self,

        num_classes,

        freeze_backbone=True

    ):

        self.num_classes = num_classes

        self.freeze_backbone = freeze_backbone

    def build(self):

        model = TransferLearningNetwork(

            self.num_classes,

            self.freeze_backbone

        )

        Logger.success(
            "Transfer Learning model created."
        )

        return model