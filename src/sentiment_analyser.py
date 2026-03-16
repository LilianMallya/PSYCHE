import requests
import config

class SentimentAnalyser:
  

    HF_API_URL = "https://api-inference.huggingface.co/models/"

    POSITIVE_WORDS = ["excellent", "great", "outstanding", "innovative", "passionate",
                      "dedicated", "thriving", "success", "achieve", "growth"]
    NEGATIVE_WORDS = ["difficult", "challenging", "concerning", "risk", "pressure",
                      "stress", "decline", "fail", "problem", "issue"]

    def __init__(self, text: str):
        self.text = text
        self.headers = {"Authorization": f"Bearer {config.HUGGINGFACE_API_KEY}"}

    def _call_hf_api(self, model: str, text: str) -> list:
        url = self.HF_API_URL + model
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json={"inputs": text[:512]},
                timeout=25
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            return None
        return None

    def _lexicon_fallback(self) -> dict:
        words = self.text.lower().split()
        pos = sum(1 for w in words if w in self.POSITIVE_WORDS)
        neg = sum(1 for w in words if w in self.NEGATIVE_WORDS)
        total = max(pos + neg, 1)
        return {
            "positive": round(pos / total, 3),
            "negative": round(neg / total, 3),
            "neutral": round(1 - (pos + neg) / total, 3),
            "source": "lexicon_fallback"
        }

    def get_sentiment(self) -> dict:
        result = self._call_hf_api(config.SENTIMENT_MODEL, self.text)
        if result:
            scores = {item["label"].lower(): round(item["score"], 3)
                      for item in result[0]}
            scores["source"] = "huggingface"
            return scores
        return self._lexicon_fallback()

    def get_emotion(self) -> dict:
        result = self._call_hf_api(config.EMOTION_MODEL, self.text)
        if result:
            return {item["label"].lower(): round(item["score"], 3)
                    for item in result[0]}
        return {}

    def dominant_emotion(self) -> str:
        emotions = self.get_emotion()
        if not emotions:
            return "unknown"
        return max(emotions, key=emotions.get)
