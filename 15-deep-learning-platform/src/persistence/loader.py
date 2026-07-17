import torch
import json
import pickle
from config import settings
from src.utils.logger import Logger


class ModelLoader:

    @staticmethod
    def load(model):

        checkpoint = settings.MODELS_DIR / "best_model.pth"

        model.load_state_dict(

            torch.load(

                checkpoint,

                map_location=settings.DEVICE

            )

        )

        Logger.success(

            "Best model loaded."

        )

        with open(

            settings.MODELS_DIR /

            "class_names.pkl",

            "rb"

        ) as file:

            class_names = pickle.load(file)

        with open(

            settings.MODELS_DIR /

            "config.json"

        ) as file:

            config = json.load(file)

        return {

            "model": model,

            "classes": class_names,

            "config": config

        }