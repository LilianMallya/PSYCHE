from pathlib import Path

from utils.helpers import load_json_file


class PersuasionAnalyser:
 

    LEXICON_PATH = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "lexicons"
        / "persuasion_markers.json"
    )
    DEFAULT_PRINCIPLES = {
        "reciprocity": {
            "markers": ["free", "gift", "offer", "bonus", "complimentary",
                        "give", "provide", "benefit", "reward"],
            "description": "Creates obligation through offering something first."
        },
        "commitment": {
            "markers": ["commit", "promise", "pledge", "dedicated", "consistent",
                        "loyal", "stand by", "believe in", "mission"],
            "description": "Appeals to consistency with stated values or past actions."
        },
        "social_proof": {
            "markers": ["thousands", "customers", "clients", "users", "reviews",
                        "trusted by", "community", "members", "followers"],
            "description": "Uses others' behaviour to validate choices."
        },
        "authority": {
            "markers": ["years of experience", "expert", "leader", "award",
                        "recognised", "certified", "qualified", "specialist"],
            "description": "Establishes credibility through expertise signals."
        },
        "liking": {
            "markers": ["you", "your", "we", "together", "our", "share",
                        "connect", "like you", "understand", "relate"],
            "description": "Builds rapport and similarity with the reader."
        },
        "scarcity": {
            "markers": ["limited", "exclusive", "only", "now", "today",
                        "last", "hurry", "deadline", "urgent", "closing"],
            "description": "Creates urgency through perceived rarity or time pressure."
        }
    }
    PRINCIPLES = load_json_file(str(LEXICON_PATH), DEFAULT_PRINCIPLES)

    def __init__(self, text: str):
        self.text = text.lower()

    def analyse(self) -> dict:
        results = {}
        for principle, data in self.PRINCIPLES.items():
            found = [m for m in data["markers"] if m in self.text]
            score = min(len(found) / 4, 1.0)
            results[principle] = {
                "score": round(score, 3),
                "found_markers": found,
                "description": data["description"]
            }
        return results

    def dominant_principle(self) -> str:
        results = self.analyse()
        return max(results, key=lambda k: results[k]["score"])
