from collections import Counter

from src.preprocessing.text_preprocessor import TextPreprocessor


class Tokenizer:

    def __init__(

        self,

        max_length=128

    ):

        self.preprocessor = TextPreprocessor()

        self.max_length = max_length

        self.vocabulary = {

            "<PAD>": 0,

            "<UNK>": 1

        }

    def tokenize(self, text):

        text = self.preprocessor.clean(text)

        return text.split()

    def fit(self, texts):

        counter = Counter()

        for text in texts:

            counter.update(

                self.tokenize(text)

            )

        for word, _ in counter.items():

            if word not in self.vocabulary:

                self.vocabulary[word] = len(

                    self.vocabulary

                )

    @property
    def vocabulary_size(self):

        return len(self.vocabulary)

    def encode(self, text):

        tokens = self.tokenize(text)

        indices = [

            self.vocabulary.get(

                token,

                self.vocabulary["<UNK>"]

            )

            for token in tokens

        ]

        if len(indices) < self.max_length:

            indices.extend(

                [0] *

                (

                    self.max_length -

                    len(indices)

                )

            )

        else:

            indices = indices[:self.max_length]

        return indices