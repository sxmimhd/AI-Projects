from src.models.transfer_learning import TransferLearningModel


class ModelFactory:

    @staticmethod
    def create(

        model_name,

        num_classes

    ):

        if model_name == "TransferLearningModel":

            return TransferLearningModel(

                num_classes=num_classes

            ).build()

        raise ValueError(

            f"{model_name} not implemented."

        )