# PSYCHE

PSYCHE is a text analysis tool that extracts psychological signals from writing.

The system analyzes:
- personality signals (Big Five)
- persuasion techniques
- cognitive bias markers
- emotional tone
- language style

The goal is to explore how linguistic patterns reflect psychological framing in text.

## Demo

<video controls width="900" preload="metadata">
  <source src="https://drive.google.com/uc?export=download&id=1X8liubk-bk5Ll_6ic2VIlKeypHJuC7ie" type="video/mp4">
  Your browser does not support the video tag.
</video>

Direct link: [Project Demo](https://drive.google.com/file/d/1X8liubk-bk5Ll_6ic2VIlKeypHJuC7ie/view?usp=sharing)

## Project Structure

psyche/
- src/ (core analysis modules)
- utils/ (shared helpers)
- tests/ (pytest)
- assets/sample_inputs/ (demo texts)
- assets/lexicons/ (JSON marker lists)
- docs/ (sources and design notes)
- app.py (Streamlit entry point)
- config.py (settings + thresholds)

## Setup (Mac)

```bash
cd ~/Desktop/psyche
source .venv39/bin/activate
pip install -r requirements.txt
```

Set keys in your terminal session:

```bash
export OPENAI_API_KEY="..."
export HUGGINGFACE_API_KEY="..."
```

Run:

```bash
streamlit run app.py
```

## Composite Score

Computed in `src/report_builder.py`:

score =
- sentiment_positive * WEIGHTS["sentiment"]
- openness * WEIGHTS["openness"]
- conscientiousness * WEIGHTS["conscientiousness"]
- (1 - neuroticism) * WEIGHTS["emotional_stability"]
- formality_score * WEIGHTS["language_clarity"]

Then scaled to /10:
- PsycheScore = min(score * 10, 10)

## Limitations

- This system uses heuristic markers rather than trained models.
- Detected traits represent linguistic signals rather than actual personality traits.
- Bias and persuasion markers can trigger false positives in neutral contexts.
- Do not use this tool for hiring, medical, or clinical decisions.
