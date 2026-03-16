import config
from src.text_cleaner import TextCleaner
from src.personality_analyser import PersonalityAnalyser
from src.bias_detector import BiasDetector
from src.persuasion_analyser import PersuasionAnalyser
from src.sentiment_analyser import SentimentAnalyser
from src.language_analyser import LanguageAnalyser

class ReportBuilder:
   

    def __init__(self, raw_text: str):
        self.raw_text = raw_text
        self.report = {}

    def _compute_composite_score(self, personality: dict,
                                  sentiment: dict, language: dict) -> float:
        score = 0
        score += sentiment.get("positive", 0) * config.WEIGHTS["sentiment"]
        score += personality.get("openness", 0) * config.WEIGHTS["openness"]
        score += personality.get("conscientiousness", 0) * config.WEIGHTS["conscientiousness"]
        score += (1 - personality.get("neuroticism", 0)) * config.WEIGHTS["emotional_stability"]
        score += language.get("formality_score", 0) * config.WEIGHTS["language_clarity"]
        return round(min(score * 10, 10), 2)

    def build(self) -> dict:
        cleaner = TextCleaner(self.raw_text)
        clean_text = cleaner.clean()

        if cleaner.word_count() < config.MIN_WORD_COUNT:
            return {"error": f"Text too short. Minimum {config.MIN_WORD_COUNT} words required."}

        personality = PersonalityAnalyser(clean_text).get_profile()
        biases = BiasDetector(clean_text).detect()
        persuasion = PersuasionAnalyser(clean_text).analyse()
        sa = SentimentAnalyser(clean_text)
        sentiment = sa.get_sentiment()
        emotion = sa.get_emotion()
        language = LanguageAnalyser(clean_text).get_profile()

        composite = self._compute_composite_score(personality, sentiment, language)

        self.report = {
            "meta": {
                "word_count": cleaner.word_count(),
                "sentence_count": cleaner.sentence_count(),
                "composite_score": composite
            },
            "personality": personality,
            "biases": biases,
            "persuasion": persuasion,
            "sentiment": sentiment,
            "emotion": emotion,
            "language": language
        }

        return self.report
