import streamlit as st

st.set_page_config(
    page_title="Human-AI Cognitive Toolkit",
    page_icon="🧠",
    layout="centered"
)

st.title("Human-AI Cognitive Toolkit")
st.subheader("Start an AI session with collaborative discipline")

st.write(
    "Build a starter prompt that helps you use AI as a partner, not a substitute."
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