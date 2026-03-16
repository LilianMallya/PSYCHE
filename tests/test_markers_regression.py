import pytest

from src.bias_detector import BiasDetector
from src.personality_analyser import PersonalityAnalyser
from src.persuasion_analyser import PersuasionAnalyser


@pytest.mark.parametrize(
    "text,expected_trait",
    [
        ("imagine creative curious explore novel vision innovate dream idea discover wonder possibility", "openness"),
        ("plan organise detail systematic reliable deadline structure process consistent precise responsible deliver", "conscientiousness"),
        ("team collaborate people energy lead engage network communicate together dynamic enthusiastic", "extraversion"),
        ("support help trust care empathy respect kind cooperative understand value inclusive community", "agreeableness"),
        ("stress worry pressure difficult challenge concern overwhelm uncertain anxious fear risk unstable", "neuroticism"),
        ("curious creative explore idea discover possibility and wonder about a new vision", "openness"),
        ("reliable process structure responsible precise plan around every deadline", "conscientiousness"),
        ("we collaborate and engage people with dynamic team energy", "extraversion"),
        ("we value empathy respect and inclusive community support", "agreeableness"),
        ("anxious and uncertain under stress with constant worry and pressure", "neuroticism"),
    ],
)
def test_personality_regression(text, expected_trait):
    dominant = PersonalityAnalyser(text).get_dominant_trait()
    assert dominant == expected_trait


@pytest.mark.parametrize(
    "text,expected_bias",
    [
        ("Clearly this is undeniable and obviously proven as expected.", "confirmation_bias"),
        ("This is definitely the best and absolutely perfect outcome.", "overconfidence_bias"),
        ("Limited spots left, last chance, urgent deadline, running out now.", "scarcity_bias"),
        ("According to expert scientists, research shows this is certified.", "authority_bias"),
        ("Everyone is joining, most people agree, the majority loves it.", "bandwagon_bias"),
        ("This opportunity has growth potential and future transformation.", "framing_bias"),
        ("Obviously, of course, everyone knows this is right.", "confirmation_bias"),
        ("Guaranteed results, always strong, never weak.", "overconfidence_bias"),
        ("Exclusive access, few spots, urgent action required.", "scarcity_bias"),
        ("Data shows and official reports from experts confirm this.", "authority_bias"),
    ],
)
def test_bias_regression(text, expected_bias):
    results = BiasDetector(text).detect()
    assert results[expected_bias]["detected"] is True


@pytest.mark.parametrize(
    "text,expected_principle",
    [
        ("Free gift bonus offer for you today.", "reciprocity"),
        ("We commit to this mission and promise to stay consistent.", "commitment"),
        ("Thousands of customers and users trust our community reviews.", "social_proof"),
        ("Our expert leader is certified and highly qualified.", "authority"),
        ("We understand you, share your goals, and connect together.", "liking"),
        ("Limited exclusive offer, only today, hurry before closing.", "scarcity"),
        ("Complimentary reward and free benefit for members.", "reciprocity"),
        ("Dedicated teams stand by this pledge and believe in the mission.", "commitment"),
        ("Trusted by clients, followers, and members worldwide.", "social_proof"),
        ("Specialist advice from a recognised award-winning expert.", "authority"),
    ],
)
def test_persuasion_regression(text, expected_principle):
    dominant = PersuasionAnalyser(text).dominant_principle()
    assert dominant == expected_principle
