import pandas as pd

from config import settings


class ModelSummary:

    @staticmethod
    def save(model):

        total = sum(

            p.numel()

            for p in model.parameters()

        )

        trainable = sum(

            p.numel()

            for p in model.parameters()

            if p.requires_grad

        )

        summary = pd.DataFrame({

            "Property": [

                "Total Parameters",

                "Trainable Parameters"

            ],

            "Value": [

                total,

                trainable

            ]

        })

        summary.to_csv(

            settings.METRICS_DIR /

            "model_summary.csv",

            index=False

        )