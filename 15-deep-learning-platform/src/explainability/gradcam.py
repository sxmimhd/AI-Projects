from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image

from config import settings
from src.utils.logger import Logger


class GradCAM:

    def __init__(

        self,

        model,

        transform

    ):

        self.model = model.to(settings.DEVICE)

        self.transform = transform

        self.gradients = None
        self.activations = None

        self.register_hooks()

    def register_hooks(self):

        target_layer = self.model.backbone.layer4[-1]

        target_layer.register_forward_hook(
            self.forward_hook
        )

        target_layer.register_full_backward_hook(
            self.backward_hook
        )

    def forward_hook(

        self,

        module,

        inputs,

        outputs

    ):

        self.activations = outputs

    def backward_hook(

        self,

        module,

        grad_input,

        grad_output

    ):

        self.gradients = grad_output[0]

    def generate(

        self,

        image_path

    ):

        image = Image.open(

            image_path

        ).convert("RGB")

        tensor = self.transform(image)

        tensor = tensor.unsqueeze(0).to(settings.DEVICE)

        self.model.eval()

        outputs = self.model(tensor)

        prediction = outputs.argmax(dim=1)

        self.model.zero_grad()

        outputs[0, prediction].backward()

        gradients = self.gradients.mean(

            dim=(2, 3),

            keepdim=True

        )

        activations = self.activations

        heatmap = (

            gradients *

            activations

        ).sum(

            dim=1

        ).squeeze()

        heatmap = torch.relu(

            heatmap

        )

        heatmap /= (

            heatmap.max() + 1e-8

        )

        heatmap = heatmap.cpu().numpy()

        self.save(

            image_path,

            heatmap
        )

    def save(

        self,

        image_path,

        heatmap

    ):

        image = cv2.imread(image_path)

        image = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

        heatmap = cv2.resize(

            heatmap,

            (

                image.shape[1],

                image.shape[0]

            )

        )

        heatmap = np.uint8(

            255 *

            heatmap

        )

        heatmap = cv2.applyColorMap(

            heatmap,

            cv2.COLORMAP_JET

        )

        heatmap = cv2.cvtColor(

            heatmap,

            cv2.COLOR_BGR2RGB

        )

        overlay = cv2.addWeighted(

            image,

            0.6,

            heatmap,

            0.4,

            0

        )

        plt.figure(

            figsize=(6, 6)

        )

        plt.imshow(

            overlay

        )

        plt.axis("off")

        plt.tight_layout()

        output_path = (

            settings.EXPLAINABILITY_DIR /

            "gradcam.png"

        )

        plt.savefig(

            output_path,

            dpi=300

        )

        plt.close()

        Logger.success(

            "GradCAM saved."
        )