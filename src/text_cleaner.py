import re

class TextCleaner:
    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.cleaned_text = ""

    def remove_urls(self, text: str) -> str:
        return re.sub(r"http\S+|www\S+", "", text)

    def remove_special_characters(self, text: str) -> str:
        return re.sub(r"[^a-zA-Z0-9\s.,!?'-]", "", text)

    def normalise_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def clean(self) -> str:
        text = self.raw_text
        text = self.remove_urls(text)
        text = self.remove_special_characters(text)
        text = self.normalise_whitespace(text)
        self.cleaned_text = text
        return self.cleaned_text

    def word_count(self) -> int:
        return len(self.cleaned_text.split())

    def sentence_count(self) -> int:
        return len(re.split(r'[.!?]+', self.cleaned_text))
