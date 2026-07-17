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

        class_names=None

    ):

        self.model = model.to(settings.DEVICE)

        self.test_loader = test_loader

        self.class_names = class_names

        self.binary = (

            model.__class__.__name__

            == "SentimentNetwork"

        )


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

                if self.binary:

                    probs = torch.sigmoid(outputs)

                    preds = (

                        probs > 0.5

                    ).long()

                    predictions.extend(

                        preds.cpu().numpy().flatten()

                    )

                    labels.extend(

                        targets.cpu().numpy()

                    )

                    probabilities.extend(

                        probs.cpu().numpy().flatten()

                    )

                else:

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

                    predictions.extend(

                        preds.cpu().numpy()

                    )

                    labels.extend(

                        targets.cpu().numpy()

                    )

                    probabilities.extend(

                        probs.max(dim=1)[0].cpu().numpy()

                    )

                total += targets.size(0)

        accuracy = accuracy_score(

            labels,

            predictions

        )

        if self.binary:

            top5_accuracy = None

        else:

            top5_accuracy = top5_correct / total

        if self.binary:

            report = classification_report(

                labels,

                predictions,

                output_dict=True

            )

        else:

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

        if self.binary:

            Logger.info(

                f"Test Accuracy : {accuracy:.4f}"

            )

        else:

            Logger.info(

                f"Test Accuracy : {accuracy:.4f} | "

                f"Top-5 Accuracy : {top5_accuracy:.4f}"

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