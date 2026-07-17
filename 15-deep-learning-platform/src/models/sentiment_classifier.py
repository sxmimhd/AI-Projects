import torch

import torch.nn as nn

from src.utils.logger import Logger


class SentimentNetwork(nn.Module):

    def __init__(

        self,

        vocabulary_size,

        embedding_dim,

        hidden_dim

    ):

        super().__init__()

        self.embedding = nn.Embedding(
            vocabulary_size,
            embedding_dim,
            padding_idx=0
        )

        self.pool = nn.AdaptiveAvgPool1d(1)

        self.fc1 = nn.Linear(
            embedding_dim,
            hidden_dim
        )

        self.dropout = nn.Dropout(0.3)

        self.fc2 = nn.Linear(
            hidden_dim,
            1
        )

    def forward(self, x):

        x = self.embedding(x)

        x = x.permute(0, 2, 1)

        x = self.pool(x).squeeze(-1)

        x = torch.relu(
            self.fc1(x)
        )

        x = self.dropout(x)

        return self.fc2(x)


class SentimentClassifier:

    def __init__(

        self,

        vocabulary_size,

        embedding_dim=128,

        hidden_dim=128

    ):

        self.vocabulary_size = vocabulary_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim

    def build(self):

        Logger.success(
            "Sentiment model created."
        )

        return SentimentNetwork(

            self.vocabulary_size,

            self.embedding_dim,

            self.hidden_dim

        )