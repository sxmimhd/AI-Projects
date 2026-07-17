import re

from src.utils.logger import Logger


class TextPreprocessor:

    def __init__(self):

        pass


    def clean(self, text):

        text = text.lower()

        text = re.sub(r"http\S+", "", text)

        text = re.sub(r"<.*?>", "", text)

        text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()


    def build(self):

        Logger.success(
            "Text preprocessing pipeline created."
        )

        return self