import torch

from torch.utils.data import Dataset


class TextDataset(Dataset):

    def __init__(
        self,
        dataframe,
        tokenizer,
        text_column,
        target_column
    ):

        self.df = dataframe.reset_index(drop=True)

        self.tokenizer = tokenizer

        self.text_column = text_column

        self.target_column = target_column

    def __len__(self):

        return len(self.df)

    def __getitem__(self, index):

        text = self.df.loc[index, self.text_column]

        label = self.df.loc[index, self.target_column]

        tokens = self.tokenizer.encode(text)

        return (

            torch.tensor(tokens),

            torch.tensor(label).float()

        )