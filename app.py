import streamlit as st


st.set_page_config(
    page_title="Human-AI Cognitive Toolkit",
    page_icon="🧠",
    layout="centered"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap');

    section[data-testid="stSidebar"] {
        background-color: #171f5f;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #171f5f;
    }

    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0rem;
    }

    .stApp {
        background: #171f5f;
        color: #f7f3ee;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero-kicker {
        color: #50d9f3;
        text-align: center;
        font-size: 0.85rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1.25rem;
    }

    .hero-title {
        text-align: center;
        margin: 0 auto 0.75rem auto;
    }

    .hero-line {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        line-height: 1.05;
        letter-spacing: -0.04em;
        font-weight: 800;
        display: block;
    }

    .hero-line.white {
        color: #f7f3ee;
    }

    .hero-line.blue {
        color: #4a8dff;
    }

    .hero-line.cyan {
        color: #50d9f3;
    }

    .hero-subtitle {
        color: #f1eef2;
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.45;
        max-width: 760px;
        margin: 1.25rem auto 2rem auto;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #50d9f3;
        letter-spacing: 0.02em;
    }

    p, label, .stMarkdown {
        color: #f1eef2;
        font-family: 'Inter', sans-serif;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #50d9f3, #4a72ff, transparent);
        margin: 1.75rem 0;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea {
        background-color: #f7f3ee;
        color: #111827;
        border-radius: 12px;
        border: 1px solid #50d9f3;
    }

    pre {
        background-color: #0f1648 !important;
        border: 1px solid #50d9f3;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 0 24px rgba(80, 217, 243, 0.12);
    }

    code {
        color: #f7f3ee !important;
        font-family: 'Inter', sans-serif !important;
        white-space: pre-wrap !important;
    }

    .stCaption, caption {
        color: #8edff0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="hero-kicker">FIRST [AI]D FOR YOUR MIND</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-title">
        <div class="hero-line white">Your Mind.</div>
        <div class="hero-line blue">Your Rules.</div>
        <div class="hero-line cyan">In the Age of AI.</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        Build a short starter prompt that helps you use AI with reflection,
        source awareness, and collaborative discipline.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


session_purpose = st.selectbox(
    "What are you using AI for?",
    [
        "Learn something",
        "Brainstorm ideas",
        "Fact-check or research",
        "Make a decision",
        "Improve writing",
        "Solve a problem",
    ]
)

ai_role = st.selectbox(
    "What role should the AI take?",
    [
        "Patient tutor",
        "Critical thinking partner",
        "Research assistant",
        "Creative collaborator",
        "Decision-support analyst",
    ]
)

human_context = st.text_area(
    "Human context",
    placeholder="What do you already know, feel, believe, or need the AI to understand?"
)

source_expectation = st.selectbox(
    "How should the AI handle facts and uncertainty?",
    [
        "General explanation is fine",
        "Separate facts from assumptions",
        "Tell me what needs verification",
        "Ask for sources or citations",
        "Show opposing views or missing context",
    ]
)

answer_style = st.selectbox(
    "How should the AI answer?",
    [
        "Simple beginner explanation",
        "Step-by-step",
        "Balanced pros and cons",
        "Challenge my assumptions",
        "Give me options, but let me decide",
    ]
)

generated_prompt = f"""
You are acting as a {ai_role}.

I am using AI for this purpose:
{session_purpose}

Here is my human context:
{human_context if human_context else "[No human context provided yet. Help me clarify what context may matter.]"}

When answering, follow these rules:
- Help me think better, not just faster.
- Separate facts, assumptions, opinions, and uncertainty when relevant.
- Tell me what needs verification.
- Point out missing context or possible blind spots.
- Do not make the final decision for me.
- Preserve my role as the final interpreter.

My source and evidence expectation:
{source_expectation}

Preferred answer style:
{answer_style}
"""

st.divider()

st.header("Generated Starter Prompt")

st.write("Copy this prompt into your LLM:")

st.code(
    generated_prompt.strip(),
    language="text"
)

st.caption(
    "Human reminder: AI is a partner, not a substitute. You remain responsible for judgment, meaning, and action."
)