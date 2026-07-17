import matplotlib.pyplot as plt

from sklearn.metrics import ConfusionMatrixDisplay

from config import settings


class TrainingPlots:

    @staticmethod
    def confusion_matrix(

        matrix,

        class_names

    ):

        fig, ax = plt.subplots(

            figsize=(8,8)

        )

        ConfusionMatrixDisplay(

            matrix,

            display_labels=class_names

        ).plot(

            cmap="Blues",

            ax=ax,

            colorbar=False

        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(

            settings.FIGURES_DIR /

            "confusion_matrix.png",

            dpi=300

        )

        plt.close()

    @staticmethod
    def history(history):

        plt.figure(figsize=(8,5))

        plt.plot(

            history["Epoch"],

            history["Train Loss"],

            label="Train"

        )

        plt.plot(

            history["Epoch"],

            history["Validation Loss"],

            label="Validation"

        )

        plt.legend()

        plt.xlabel("Epoch")

        plt.ylabel("Loss")

        plt.tight_layout()

        plt.savefig(

            settings.FIGURES_DIR /

            "training_loss.png",

            dpi=300

        )

        plt.close()