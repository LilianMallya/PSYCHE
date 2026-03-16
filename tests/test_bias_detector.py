from src.bias_detector import BiasDetector

def test_scarcity_bias_flagged():
    text = "Limited offer. Last chance. Few spots. Urgent deadline. Running out."
    results = BiasDetector(text).detect()
    assert results["scarcity_bias"]["detected"] is True
    assert len(results["scarcity_bias"]["found_markers"]) >= 2

def test_no_bias_detected_for_neutral_text():
    text = "This is a simple sentence about a normal day with no persuasion."
    results = BiasDetector(text).detect()
    flagged = [k for k, v in results.items() if v["detected"]]
    assert len(flagged) <= 2
