import re

class LanguageAnalyser:
  

    FORMAL_MARKERS = ["therefore", "furthermore", "consequently", "regarding",
                      "hereby", "pursuant", "aforementioned", "henceforth"]
    CASUAL_MARKERS = ["basically", "kind of", "sort of", "you know", "like",
                      "stuff", "things", "pretty much", "a lot"]
    CERTAINTY_MARKERS = ["will", "must", "definitely", "certainly", "always",
                         "guaranteed", "without doubt", "clearly"]
    UNCERTAINTY_MARKERS = ["might", "could", "perhaps", "possibly", "maybe",
                           "seems", "appears", "suggest", "indicate"]

    def __init__(self, text: str):
        self.text = text
        self.words = text.lower().split()
        self.sentences = re.split(r'[.!?]+', text)
        self.word_count = len(self.words)

    def avg_word_length(self) -> float:
        lengths = [len(w) for w in self.words if w.isalpha()]
        return round(sum(lengths) / max(len(lengths), 1), 2)

    def avg_sentence_length(self) -> float:
        lengths = [len(s.split()) for s in self.sentences if s.strip()]
        return round(sum(lengths) / max(len(lengths), 1), 2)

    def formality_score(self) -> float:
        formal = sum(1 for m in self.FORMAL_MARKERS if m in self.text.lower())
        casual = sum(1 for m in self.CASUAL_MARKERS if m in self.text.lower())
        return round(formal / max(formal + casual, 1), 3)

    def certainty_score(self) -> float:
        certain = sum(1 for m in self.CERTAINTY_MARKERS if m in self.text.lower())
        uncertain = sum(1 for m in self.UNCERTAINTY_MARKERS if m in self.text.lower())
        return round(certain / max(certain + uncertain, 1), 3)

    def first_person_ratio(self) -> float:
        first_person = len(re.findall(r'\b(i|me|my|myself|mine)\b', self.text.lower()))
        collective = len(re.findall(r'\b(we|us|our|ourselves)\b', self.text.lower()))
        total = max(first_person + collective, 1)
        return round(first_person / total, 3)

    def get_profile(self) -> dict:
        avg_len = self.avg_word_length()
        complexity = (
            "high" if avg_len > 5.5 else
            "medium" if avg_len > 4.5 else
            "low"
        )
        return {
            "avg_word_length": avg_len,
            "avg_sentence_length": self.avg_sentence_length(),
            "formality_score": self.formality_score(),
            "certainty_score": self.certainty_score(),
            "first_person_ratio": self.first_person_ratio(),
            "complexity_label": complexity
        }
