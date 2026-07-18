from pathlib import Path

import pandas as pd
import torch
from PIL import Image

from config import settings
from src.utils.logger import Logger
from src.explainability.gradcam import GradCAM


class Predictor:

    def __init__(

        self,

        model,

        transform,

        class_names

    ):

        self.model = model.to(settings.DEVICE)

        self.transform = transform

        self.class_names = class_names

    def predict(

        self,

        image_path,

        explain=False

    ):

        image = Image.open(image_path).convert("RGB")

        tensor = self.transform(image)

        tensor = tensor.unsqueeze(0).to(settings.DEVICE)

        self.model.eval()

        with torch.no_grad():

            outputs = self.model(tensor)

            probabilities = torch.softmax(

                outputs,

                dim=1

            )

            confidence, prediction = probabilities.max(dim=1)

        result = {

            "image": Path(image_path).name,

            "prediction": self.class_names[prediction.item()],

            "confidence": confidence.item()

        }

        Logger.success("Prediction completed.")

        Logger.info(
            f"{result['prediction']} | Confidence : {result['confidence']:.4f}"
        )

        #if explain:

        #    gradcam = GradCAM(

        #        self.model,

        #        self.transform

        #    )

        #    gradcam.generate(image_path)

        return result

    def predict_folder(self, folder):

        results = []

        for image in Path(folder).glob("*"):

            if image.suffix.lower() not in [

                ".png",

                ".jpg",

                ".jpeg"

            ]:

                continue

            results.append(

                self.predict(image)

            )

        dataframe = pd.DataFrame(results)

        dataframe.to_csv(

            settings.PREDICTIONS_DIR /

            "folder_predictions.csv",

            index=False

        )

        Logger.success(

            "Folder prediction completed."

        )

        return dataframe
    
    def predict_text(self, sentence):

        self.model.eval()

        tokens = self.transform.encode(sentence)

        tensor = torch.tensor(
            tokens
        ).unsqueeze(0).to(settings.DEVICE)

        with torch.no_grad():

            output = self.model(tensor)

            probability = torch.sigmoid(output)

            confidence = probability.item()

        prediction = int(confidence >= 0.5)

        result = {

            "sentence": sentence,

            "prediction": prediction,

            "confidence": confidence

        }

        Logger.success("Prediction completed.")

        Logger.info(
            f"Prediction : {prediction} | Confidence : {confidence:.4f}"
        )

        return result