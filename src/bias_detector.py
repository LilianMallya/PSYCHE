from pathlib import Path

from utils.helpers import load_json_file


class BiasDetector:
   

    LEXICON_PATH = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "lexicons"
        / "bias_markers.json"
    )
    DEFAULT_PATTERNS = {
        "confirmation_bias": {
            "markers": ["clearly", "obviously", "everyone knows", "as expected",
                        "proven", "undeniable", "of course", "naturally"],
            "description": "Tendency to favour information confirming existing beliefs."
        },
        "overconfidence_bias": {
            "markers": ["definitely", "certainly", "guaranteed", "always", "never",
                        "best", "perfect", "flawless", "absolutely"],
            "description": "Excessive certainty in claims or outcomes."
        },
        "scarcity_bias": {
            "markers": ["limited", "exclusive", "rare", "only", "last chance",
                        "urgent", "deadline", "running out", "few spots"],
            "description": "Urgency created by perceived scarcity."
        },
        "authority_bias": {
            "markers": ["expert", "research shows", "studies prove", "scientists",
                        "according to", "data shows", "official", "certified"],
            "description": "Undue weight given to authority figures or credentials."
        },
        "bandwagon_bias": {
            "markers": ["everyone", "most people", "thousands", "popular",
                        "widely", "join", "community", "majority"],
            "description": "Influence from perceived social consensus."
        },
        "framing_bias": {
            "markers": ["opportunity", "growth", "challenge", "investment",
                        "potential", "future", "transformation"],
            "description": "Positive reframing of neutral or negative situations."
        }
    }
    BIAS_PATTERNS = load_json_file(str(LEXICON_PATH), DEFAULT_PATTERNS)

    def __init__(self, text: str):
        self.text = text.lower()
        self.words = self.text.split()

    def detect(self) -> dict:
        results = {}
        for bias_name, bias_data in self.BIAS_PATTERNS.items():
            found_markers = [m for m in bias_data["markers"] if m in self.text]
            score = min(len(found_markers) / 3, 1.0)
            results[bias_name] = {
                "score": round(score, 3),
                "found_markers": found_markers,
                "description": bias_data["description"],
                "detected": score > 0.2
            }
        return results

    def get_flagged_biases(self) -> list:
        detected = self.detect()
        return [name for name, data in detected.items() if data["detected"]]

    def overall_bias_score(self) -> float:
        detected = self.detect()
        scores = [d["score"] for d in detected.values()]
        return round(sum(scores) / len(scores), 3)
