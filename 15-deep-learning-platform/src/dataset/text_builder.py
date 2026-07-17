from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from src.dataset.text_dataset import TextDataset
from src.utils.logger import Logger
from config import settings


class TextDatasetBuilder:

    def __init__(
        self,
        dataframe,
        tokenizer,
        text_column,
        target_column
    ):

        self.dataframe = dataframe
        self.tokenizer = tokenizer
        self.text_column = text_column
        self.target_column = target_column

    def build(self):

        train_df, temp_df = train_test_split(
            self.dataframe,
            test_size=0.30,
            random_state=42,
            stratify=self.dataframe[self.target_column]
        )

        validation_df, test_df = train_test_split(
            temp_df,
            test_size=0.50,
            random_state=42,
            stratify=temp_df[self.target_column]
        )

        train_dataset = TextDataset(
            train_df,
            self.tokenizer,
            self.text_column,
            self.target_column
        )

        validation_dataset = TextDataset(
            validation_df,
            self.tokenizer,
            self.text_column,
            self.target_column
        )

        test_dataset = TextDataset(
            test_df,
            self.tokenizer,
            self.text_column,
            self.target_column
        )

        Logger.success("Text dataset split completed.")

        return {

            "train": DataLoader(
                train_dataset,
                batch_size=settings.BATCH_SIZE,
                shuffle=True
            ),

            "validation": DataLoader(
                validation_dataset,
                batch_size=settings.BATCH_SIZE,
                shuffle=False
            ),

            "test": DataLoader(
                test_dataset,
                batch_size=settings.BATCH_SIZE,
                shuffle=False
            )

        }