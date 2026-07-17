from collections import Counter
import pickle

from config import settings


class Vocabulary:

    def __init__(self):

        self.word_to_index = {
            "<PAD>": 0,
            "<UNK>": 1
        }

        self.index_to_word = {
            0: "<PAD>",
            1: "<UNK>"
        }

    def build(self, texts):

        counter = Counter()

        for tokens in texts:
            counter.update(tokens)

        for word in counter:

            if word not in self.word_to_index:

                index = len(self.word_to_index)

                self.word_to_index[word] = index
                self.index_to_word[index] = word

    def encode(self, tokens):

        return [

            self.word_to_index.get(

                token,

                self.word_to_index["<UNK>"]

            )

            for token in tokens

        ]

    def __len__(self):

        return len(self.word_to_index)

    def save(self):

        with open(
            settings.MODELS_DIR / "vocabulary.pkl",
            "wb"
        ) as file:

            pickle.dump(
                self.word_to_index,
                file
            )