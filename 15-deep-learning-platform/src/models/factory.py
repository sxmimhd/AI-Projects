from src.models.transfer_learning import TransferLearningModel
from src.models.cnn import CNNModel
from src.models.sentiment_classifier import SentimentClassifier

class ModelFactory:

    @staticmethod
    def create(

        model_name,

        num_classes=None,

        vocabulary_size=None

    ):

        if model_name == "TransferLearningModel":

            return TransferLearningModel(

                num_classes=num_classes

            ).build()

        elif model_name == "CNNModel":

            return CNNModel(

                num_classes

            ).build()

        elif model_name == "SentimentClassifier":

            return SentimentClassifier(

                vocabulary_size=vocabulary_size

            ).build()

        raise ValueError(

            f"{model_name} not implemented."

        )
    