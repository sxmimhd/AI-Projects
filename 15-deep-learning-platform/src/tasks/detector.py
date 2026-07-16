from src.utils.logger import Logger


class TaskDetector:

    def __init__(self, dataset_type):

        self.dataset_type = dataset_type

        self.task = None

        self.model_family = None


    def detect(self):

        if self.dataset_type == "vision":

            self.task = "Image Classification"

            self.model_family = "Transfer Learning"

        elif self.dataset_type == "nlp":

            self.task = "Binary Text Classification"

            self.model_family = "Embedding Network"

        else:

            raise ValueError("Unknown dataset type.")

        Logger.success("Task detected successfully.")

        Logger.info(f"Task : {self.task}")

        Logger.info(f"Recommended Model : {self.model_family}")

        return {

            "task": self.task,

            "model_family": self.model_family

        }