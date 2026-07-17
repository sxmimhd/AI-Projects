import json
import pickle
import torch

from config import settings
from src.utils.logger import Logger


class ModelSaver:

    @staticmethod
    def save(

        model,

        class_names,

        config

    ):

        torch.save(

            model.state_dict(),

            settings.MODELS_DIR /

            "best_model.pth"

        )

        with open(

            settings.MODELS_DIR /

            "class_names.pkl",

            "wb"

        ) as file:

            pickle.dump(

                class_names,

                file

            )

        with open(

            settings.MODELS_DIR /

            "config.json",

            "w"

        ) as file:

            json.dump(

                config,

                file,

                indent=4

            )

        Logger.success(

            "Model package exported."
        )