import os

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Model settings
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"

# Analysis thresholds
HIGH_TRAIT_THRESHOLD = 0.65
LOW_TRAIT_THRESHOLD = 0.35
BIAS_CONFIDENCE_THRESHOLD = 0.50

# Text constraints
MIN_WORD_COUNT = 20
MAX_WORD_COUNT = 2000

# Scoring weights for composite score
WEIGHTS = {
    "sentiment": 0.20,
    "openness": 0.15,
    "conscientiousness": 0.20,
    "emotional_stability": 0.20,
    "language_clarity": 0.15,
    "persuasion_transparency": 0.10,
}

# UI
APP_TITLE = "PSYCHE"
APP_SUBTITLE = "Psychological Intelligence & Character Heuristics Engine"
