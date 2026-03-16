from pathlib import Path

from utils.helpers import load_json_file

class PersonalityAnalyser:


    LEXICON_PATH = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "lexicons"
        / "personality_markers.json"
    )
    DEFAULT_MARKERS = {
        "openness": [
            "imagine", "creative", "curious", "explore", "novel", "vision",
            "innovate", "dream", "idea", "discover", "possibility", "wonder"
        ],
        "conscientiousness": [
            "plan", "organise", "detail", "systematic", "reliable", "deadline",
            "structure", "process", "consistent", "precise", "responsible", "deliver"
        ],
        "extraversion": [
            "team", "collaborate", "people", "energy", "lead", "engage",
            "network", "communicate", "together", "dynamic", "enthusiastic"
        ],
        "agreeableness": [
            "support", "help", "trust", "care", "empathy", "respect",
            "kind", "cooperative", "understand", "value", "inclusive", "community"
        ],
        "neuroticism": [
            "stress", "worry", "pressure", "difficult", "challenge", "concern",
            "overwhelm", "uncertain", "anxious", "fear", "risk", "unstable"
        ],
    }
    MARKERS = load_json_file(str(LEXICON_PATH), DEFAULT_MARKERS)

    def __init__(self, text: str):
        self.text = text.lower()
        self.words = self.text.split()
        self.word_count = len(self.words)

    def _score_trait(self, markers: list) -> float:
        """marker frequency normalized by word count."""
        count = sum(1 for word in self.words if word in markers)
        raw_score = count / max(self.word_count, 1)
        return min(raw_score * 100, 1.0)

    def openness(self) -> float:
        return self._score_trait(self.MARKERS.get("openness", []))

    def conscientiousness(self) -> float:
        return self._score_trait(self.MARKERS.get("conscientiousness", []))

    def extraversion(self) -> float:
        return self._score_trait(self.MARKERS.get("extraversion", []))

    def agreeableness(self) -> float:
        return self._score_trait(self.MARKERS.get("agreeableness", []))

    def neuroticism(self) -> float:
        return self._score_trait(self.MARKERS.get("neuroticism", []))

    def get_profile(self) -> dict:
        return {
            "openness": round(self.openness(), 3),
            "conscientiousness": round(self.conscientiousness(), 3),
            "extraversion": round(self.extraversion(), 3),
            "agreeableness": round(self.agreeableness(), 3),
            "neuroticism": round(self.neuroticism(), 3),
        }

    def get_dominant_trait(self) -> str:
        profile = self.get_profile()
        return max(profile, key=profile.get)
