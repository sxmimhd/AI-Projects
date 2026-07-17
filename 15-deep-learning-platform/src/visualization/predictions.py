import matplotlib.pyplot as plt
import pandas as pd

from config import settings


class PredictionPlots:

    @staticmethod
    def confidence():

        df = pd.read_csv(

            settings.PREDICTIONS_DIR /

            "predictions.csv"

        )

        plt.figure(

            figsize=(8,5)

        )

        plt.hist(

            df["Confidence"],

            bins=20

        )

        plt.title(

            "Prediction Confidence Distribution"

        )

        plt.xlabel(

            "Confidence"

        )

        plt.ylabel(

            "Images"

        )

        plt.tight_layout()

        plt.savefig(

            settings.FIGURES_DIR /

            "prediction_confidence.png"

        )

        plt.close()