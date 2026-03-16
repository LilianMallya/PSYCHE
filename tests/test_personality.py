from src.personality_analyser import PersonalityAnalyser

def test_openness_markers():
    text = "Imagine a creative idea to explore a novel possibility and discover wonder"
    profile = PersonalityAnalyser(text).get_profile()
    assert profile["openness"] > 0

def test_dominant_trait_key():
    text = "plan organise detail structure process reliable deadline deliver"
    pa = PersonalityAnalyser(text)
    dom = pa.get_dominant_trait()
    assert dom in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
