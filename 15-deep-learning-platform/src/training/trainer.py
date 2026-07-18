from pathlib import Path

import pandas as pd
import torch

from config import settings

from src.utils.logger import Logger


class Trainer:

    def __init__(

        self,

        model,

        train_loader,

        validation_loader

    ):

        self.model = model.to(settings.DEVICE)

        self.train_loader = train_loader
        self.validation_loader = validation_loader

        self.optimizer = torch.optim.Adam(

            filter(

                lambda p: p.requires_grad,

                self.model.parameters()

            ),

            lr=settings.LEARNING_RATE

        )

        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(

            self.optimizer,

            mode="min",

            factor=0.5,

            patience=2

        )

        if model.__class__.__name__ == "SentimentNetwork":

            self.loss_function = torch.nn.BCEWithLogitsLoss()

            self.binary = True

        else:

            self.loss_function = torch.nn.CrossEntropyLoss()

            self.binary = False

        self.history = []

        self.best_validation_loss = float("inf")

    def train(self):

        Logger.success("Training started.")

        for epoch in range(settings.EPOCHS):

            train_loss, train_accuracy = self.train_epoch()

            validation_loss, validation_accuracy = self.validate()

            self.scheduler.step(validation_loss)

            self.history.append({

                "Epoch": epoch + 1,

                "Train Loss": train_loss,

                "Validation Loss": validation_loss,

                "Train Accuracy": train_accuracy,

                "Validation Accuracy": validation_accuracy,

                "Learning Rate":

                self.optimizer.param_groups[0]["lr"]

            })

            Logger.info(

                f"Epoch [{epoch+1}/{settings.EPOCHS}] "

                f"Train Loss {train_loss:.4f} "

                f"Validation Loss {validation_loss:.4f} "

                f"Train Acc {train_accuracy:.4f} "

                f"Validation Acc {validation_accuracy:.4f}"

            )

            if validation_loss < self.best_validation_loss:

                self.best_validation_loss = validation_loss

                torch.save(

                    self.model.state_dict(),

                    settings.MODELS_DIR / "best_model.pth"

                )

        history_df = pd.DataFrame(self.history)

        history_df.to_csv(

            settings.HISTORY_DIR / "training_history.csv",

            index=False

        )

        Logger.success("Training completed.")

        return history_df

    def train_epoch(self):

        self.model.train()

        running_loss = 0

        correct = 0

        total = 0

        for images, labels in self.train_loader:

            images = images.to(settings.DEVICE)

            labels = labels.to(settings.DEVICE)

            self.optimizer.zero_grad()

            outputs = self.model(images)

            if self.binary:

                labels = labels.float().unsqueeze(1)

                loss = self.loss_function(

                    outputs,

                    labels

                )

                predictions = (

                    torch.sigmoid(outputs) > 0.5

                ).float()

                correct += (

                    predictions == labels

                ).sum().item()

            else:

                loss = self.loss_function(

                    outputs,

                    labels

                )

                predictions = outputs.argmax(dim=1)

                correct += (

                    predictions == labels

                ).sum().item()

            loss.backward()

            self.optimizer.step()

            running_loss += loss.item()

            total += labels.size(0)

        return (

            running_loss / len(self.train_loader),

            correct / total

        )
    
    def validate(self):

        self.model.eval()

        running_loss = 0

        correct = 0

        total = 0

        with torch.no_grad():

            for images, labels in self.validation_loader:

                images = images.to(settings.DEVICE)

                labels = labels.to(settings.DEVICE)

                outputs = self.model(images)

                if self.binary:

                    labels = labels.float().unsqueeze(1)

                    loss = self.loss_function(

                        outputs,

                        labels

                    )

                    predictions = (

                        torch.sigmoid(outputs) > 0.5

                    ).float()

                    correct += (

                        predictions == labels

                    ).sum().item()

                else:

                    loss = self.loss_function(

                        outputs,

                        labels

                    )

                    predictions = outputs.argmax(dim=1)

                    correct += (

                        predictions == labels

                    ).sum().item()

                running_loss += loss.item()

                total += labels.size(0)

        return (

            running_loss / len(self.validation_loader),

            correct / total

        )
    


    