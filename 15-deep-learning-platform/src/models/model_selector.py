from src.utils.logger import Logger


class ModelSelector:

    def __init__(self, task):

        self.task = task

    def select(self):

        if self.task == "Image Classification":

            print("\nAvailable Vision Models")
            print("1. Transfer Learning")
            print("2. Custom CNN")

            choice = input("\nSelect Model: ").strip()

            if choice == "2":

                model = "CNNModel"

            else:

                model = "TransferLearningModel"

        elif self.task == "Binary Text Classification":

            print("\nAvailable NLP Models")
            print("1. Sentiment Classifier")

            input("\nPress Enter to continue...")

            model = "SentimentClassifier"

        else:

            raise ValueError("Unsupported task.")

        Logger.success("Model selected successfully.")
        Logger.info(f"Selected Model : {model}")

        return model