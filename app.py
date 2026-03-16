import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.report_builder import ReportBuilder
import config
import os

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="PSYCHE",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Cormorant+Garamond:wght@300;400;600&display=swap');

* { font-family: 'DM Mono', monospace; }

.stApp {
    background-color: #0a0e1a;
    color: #e8e8e8;
}

h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    letter-spacing: 0.05em;
}

.psyche-header {
    text-align: center;
    padding: 3rem 0 1rem 0;
    border-bottom: 1px solid #1e2540;
    margin-bottom: 2rem;
}

.psyche-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 4rem;
    font-weight: 300;
    letter-spacing: 0.4em;
    color: #c8b8ff;
    margin: 0;
}

.psyche-subtitle {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #4a5580;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.metric-card {
    background: #0f1628;
    border: 1px solid #1e2540;
    border-radius: 4px;
    padding: 1.5rem;
    margin: 0.5rem 0;
}

.score-display {
    font-size: 3rem;
    font-weight: 300;
    color: #c8b8ff;
    font-family: 'Cormorant Garamond', serif;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #4a5580;
    margin-bottom: 1rem;
}

.bias-tag {
    display: inline-block;
    background: #1a0f2e;
    border: 1px solid #3d2a6e;
    border-radius: 2px;
    padding: 0.2rem 0.6rem;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    color: #a888ff;
    margin: 0.2rem;
}

textarea {
    background-color: #0f1628 !important;
    color: #e8e8e8 !important;
    border: 1px solid #1e2540 !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

.stButton > button {
    background: #1e1035;
    color: #c8b8ff;
    border: 1px solid #3d2a6e;
    border-radius: 2px;
    letter-spacing: 0.2em;
    font-size: 0.7rem;
    text-transform: uppercase;
    padding: 0.75rem 2.5rem;
    transition: all 0.2s;
    font-family: 'DM Mono', monospace;
}

.stButton > button:hover {
    background: #2d1f50;
    border-color: #c8b8ff;
}

.stSelectbox > div > div {
    background-color: #0f1628 !important;
    border-color: #1e2540 !important;
}

.divider {
    border: none;
    border-top: 1px solid #1e2540;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────
st.markdown("""
<div class="psyche-header">
    <div class="psyche-title">PSYCHE</div>
    <div class="psyche-subtitle">Psychological Intelligence & Character Heuristics Engine</div>
</div>
""", unsafe_allow_html=True)


# ── Input Section ──────────────────────────────────────────────
col_input, col_options = st.columns([3, 1])

with col_options:
    st.markdown('<div class="section-label">Input Mode</div>', unsafe_allow_html=True)
    mode = st.selectbox("", ["Free text", "Job posting", "Company bio", "Social profile"], label_visibility="collapsed")

    st.markdown('<div class="section-label">Example Inputs</div>', unsafe_allow_html=True)
    sample_files = {
        "Job Posting": "assets/sample_inputs/job_posting.txt",
        "Company Bio": "assets/sample_inputs/company_about.txt",
        "Social Bio": "assets/sample_inputs/social_bio.txt"
    }
    selected_sample = st.selectbox("", list(sample_files.keys()), label_visibility="collapsed")

    if st.button("Load Example"):
        path = sample_files[selected_sample]
        if os.path.exists(path):
            with open(path, "r") as f:
                st.session_state["sample_text"] = f.read()

with col_input:
    st.markdown('<div class="section-label">Text Input</div>', unsafe_allow_html=True)
    default_text = st.session_state.get("sample_text", "")
    user_input = st.text_area(
        "",
        value=default_text,
        height=220,
        placeholder="Paste any text — job posting, bio, email, company statement...",
        label_visibility="collapsed"
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

analyse_btn = st.button("ANALYSE")


# ── Analysis & Results ─────────────────────────────────────────
if analyse_btn and user_input.strip():
    with st.spinner("Analysing..."):
        builder = ReportBuilder(user_input)
        report = builder.build()

    if "error" in report:
        st.error(report["error"])
    else:
        meta = report["meta"]
        personality = report["personality"]
        biases = report["biases"]
        persuasion = report["persuasion"]
        sentiment = report["sentiment"]
        emotion = report["emotion"]
        language = report["language"]

        # ── Row 1: Composite score + meta stats ────────────────
        st.markdown('<div class="section-label">Overall Assessment</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="section-label">Psyche Score</div>
                <div class="score-display">{meta['composite_score']}<span style="font-size:1rem;color:#4a5580">/10</span></div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="section-label">Word Count</div>
                <div class="score-display">{meta['word_count']}</div>
            </div>""", unsafe_allow_html=True)

        with c3:
            dominant = max(personality, key=personality.get).replace("_", " ").title()
            st.markdown(f"""
            <div class="metric-card">
                <div class="section-label">Dominant Trait</div>
                <div class="score-display" style="font-size:1.8rem">{dominant}</div>
            </div>""", unsafe_allow_html=True)

        with c4:
            dom_emotion = max(emotion, key=emotion.get) if emotion else "—"
            st.markdown(f"""
            <div class="metric-card">
                <div class="section-label">Primary Emotion</div>
                <div class="score-display" style="font-size:1.8rem">{dom_emotion.title()}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Row 2: Personality radar + sentiment bar ───────────
        col_radar, col_sent = st.columns(2)

        with col_radar:
            st.markdown('<div class="section-label">Big Five Personality Profile</div>', unsafe_allow_html=True)
            traits = list(personality.keys())
            scores = list(personality.values())
            fig_radar = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=[t.title() for t in traits] + [traits[0].title()],
                fill='toself',
                line_color='#c8b8ff',
                fillcolor='rgba(200, 184, 255, 0.15)'
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor='#0f1628',
                    radialaxis=dict(visible=True, range=[0, 1],
                                   gridcolor='#1e2540', tickfont=dict(color='#4a5580')),
                    angularaxis=dict(gridcolor='#1e2540', tickfont=dict(color='#a888ff'))
                ),
                paper_bgcolor='#0a0e1a',
                plot_bgcolor='#0a0e1a',
                margin=dict(l=40, r=40, t=20, b=20),
                height=320
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_sent:
            st.markdown('<div class="section-label">Sentiment Distribution</div>', unsafe_allow_html=True)
            sent_labels = [k for k in sentiment if k != "source"]
            sent_values = [sentiment[k] for k in sent_labels]
            fig_sent = go.Figure(go.Bar(
                x=sent_labels,
                y=sent_values,
                marker_color=['#7fffb8' if l == 'positive' else
                              '#ff7f7f' if l == 'negative' else '#4a5580'
                              for l in sent_labels]
            ))
            fig_sent.update_layout(
                paper_bgcolor='#0a0e1a',
                plot_bgcolor='#0f1628',
                font=dict(color='#4a5580'),
                xaxis=dict(gridcolor='#1e2540'),
                yaxis=dict(gridcolor='#1e2540', range=[0, 1]),
                margin=dict(l=20, r=20, t=20, b=20),
                height=320
            )
            st.plotly_chart(fig_sent, use_container_width=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Row 3: Biases + Persuasion ─────────────────────────
        col_bias, col_pers = st.columns(2)

        with col_bias:
            st.markdown('<div class="section-label">Cognitive Bias Markers</div>', unsafe_allow_html=True)
            flagged = [name for name, data in biases.items() if data["detected"]]
            if flagged:
                for b in flagged:
                    st.markdown(f'<span class="bias-tag">{b.replace("_", " ").upper()}</span>', unsafe_allow_html=True)
                    st.caption(biases[b]["description"])
                    st.caption(f"Markers found: {', '.join(biases[b]['found_markers'])}")
            else:
                st.markdown('<p style="color:#4a5580;font-size:0.8rem">No significant bias markers detected.</p>', unsafe_allow_html=True)

        with col_pers:
            st.markdown('<div class="section-label">Persuasion Techniques</div>', unsafe_allow_html=True)
            persuasion_names = list(persuasion.keys())
            persuasion_scores = [persuasion[p]["score"] for p in persuasion_names]
            fig_pers = go.Figure(go.Bar(
                x=persuasion_scores,
                y=[p.replace("_", " ").title() for p in persuasion_names],
                orientation='h',
                marker_color='#c8b8ff',
                marker_opacity=0.7
            ))
            fig_pers.update_layout(
                paper_bgcolor='#0a0e1a',
                plot_bgcolor='#0f1628',
                font=dict(color='#4a5580', size=11),
                xaxis=dict(gridcolor='#1e2540', range=[0, 1]),
                yaxis=dict(gridcolor='#1e2540'),
                margin=dict(l=20, r=20, t=10, b=10),
                height=280
            )
            st.plotly_chart(fig_pers, use_container_width=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── Row 4: Language metrics ────────────────────────────
        st.markdown('<div class="section-label">Language Profile</div>', unsafe_allow_html=True)
        lc1, lc2, lc3, lc4, lc5 = st.columns(5)
        lang_items = [
            ("Formality", language["formality_score"]),
            ("Certainty", language["certainty_score"]),
            ("Complexity", language["avg_word_length"] / 10),
            ("Self-Reference", language["first_person_ratio"]),
            ("Avg Sentence", language["avg_sentence_length"] / 30),
        ]
        for col, (label, val) in zip([lc1, lc2, lc3, lc4, lc5], lang_items):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="text-align:center">
                    <div class="section-label">{label}</div>
                    <div style="font-size:1.8rem;color:#c8b8ff;font-family:'Cormorant Garamond',serif">
                        {round(val * 100)}%
                    </div>
                </div>""", unsafe_allow_html=True)

elif analyse_btn:
    st.warning("Please enter some text to analyse.")
