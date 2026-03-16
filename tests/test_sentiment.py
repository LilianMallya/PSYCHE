from src.sentiment_analyser import SentimentAnalyser

def test_lexicon_fallback_keys(monkeypatch):
    s = SentimentAnalyser("excellent outstanding growth")
    monkeypatch.setattr(s, "_call_hf_api", lambda model, text: None)
    out = s.get_sentiment()
    assert "positive" in out and "negative" in out and "neutral" in out
    assert out["source"] == "lexicon_fallback"
