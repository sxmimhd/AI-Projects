from src.utils.logger import Logger


class ModelSelector:

    def __init__(self, task):

        self.task = task


    def select(self):

        if self.task == "Image Classification":

            model = "TransferLearningModel"

        elif self.task == "Binary Text Classification":

            model = "SentimentClassifier"

        else:

            raise ValueError("Unsupported task.")

        Logger.success("Model selected successfully.")

        Logger.info(f"Selected Model : {model}")

        return model