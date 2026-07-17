import pandas as pd
import torch

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from config import settings
from src.utils.logger import Logger


class Evaluator:

    def __init__(

        self,

        model,

        test_loader,

        class_names

    ):

        self.model = model.to(settings.DEVICE)

        self.test_loader = test_loader

        self.class_names = class_names


    def evaluate(self):

        self.model.eval()

        predictions = []

        labels = []

        probabilities = []

        top5_correct = 0

        total = 0

        with torch.no_grad():

            for images, targets in self.test_loader:

                images = images.to(settings.DEVICE)
                targets = targets.to(settings.DEVICE)

                outputs = self.model(images)

                probs = torch.softmax(

                    outputs,

                    dim=1

                )

                preds = probs.argmax(dim=1)

                top5 = outputs.topk(

                    5,

                    dim=1

                ).indices

                top5_correct += (

                    top5 == targets.unsqueeze(1)

                ).any(dim=1).sum().item()

                total += targets.size(0)

                predictions.extend(

                    preds.cpu().numpy()

                )

                labels.extend(

                    targets.cpu().numpy()

                )

                probabilities.extend(

                    probs.max(dim=1)[0].cpu().numpy()

                )

        accuracy = accuracy_score(

            labels,

            predictions

        )

        top5_accuracy = top5_correct / total

        report = classification_report(

            labels,

            predictions,

            target_names=self.class_names,

            output_dict=True

        )

        report_df = pd.DataFrame(report).transpose()

        report_df.to_csv(

            settings.METRICS_DIR /

            "classification_report.csv"

        )

        prediction_df = pd.DataFrame({

    "Actual": labels,

    "Prediction": predictions,

    "Confidence": probabilities

        })

        prediction_df.to_csv(

            settings.PREDICTIONS_DIR /

            "predictions.csv",

            index=False

        )

        Logger.success("Evaluation completed.")

        Logger.info(

            f"Test Accuracy : {accuracy:.4f} | Top-5 Accuracy : {top5_accuracy:.4f}"

        )

        metrics = pd.DataFrame({

        "Metric": [

            "Accuracy",
            "Top-5 Accuracy"

        ],

        "Value": [

            accuracy,
            top5_accuracy

        ]

        })

        metrics.to_csv(

            settings.METRICS_DIR /

            "evaluation.csv",

            index=False

        )

        return {

            "labels": labels,

            "predictions": predictions,

            "probabilities": probabilities,

            "accuracy": accuracy,

            "confusion_matrix": confusion_matrix(

                labels,

                predictions

            )

        }