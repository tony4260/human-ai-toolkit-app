import streamlit as st

from toolkit_chat import build_prompt
from toolkit_memory import CollaborationRules
from toolkit_session import render_start, render_workspace


st.set_page_config(
    page_title="Human-AI Cognitive Toolkit",
    page_icon="🧠",
    layout="centered",
)


# --------------------------------------------------
# Session state
# --------------------------------------------------
if "session_purpose" not in st.session_state:
    st.session_state.session_purpose = None


# --------------------------------------------------
# Styling
# --------------------------------------------------
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
        background-color: rgba(0, 0, 0, 0);
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0rem;
    }

    .stApp {
        background:
            radial-gradient(
                circle at top center,
                rgba(74, 141, 255, 0.08),
                transparent 34%
            ),
            #171f5f;
        color: #f7f3ee;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        max-width: 980px;
        padding-top: 1rem;
        padding-bottom: 1.5rem;
    }

    /* --------------------------------------------------
       Clean three-line outer frame
    -------------------------------------------------- */
    .page-frame {
        position: fixed;
        inset: 10px;
        border: 1px solid rgba(80, 217, 243, 0.78);
        border-radius: 18px;
        box-shadow:
            inset 0 0 0 3px rgba(74, 141, 255, 0.16),
            inset 0 0 0 7px rgba(80, 217, 243, 0.07),
            inset 0 0 30px rgba(80, 217, 243, 0.06),
            0 0 24px rgba(80, 217, 243, 0.12);
        pointer-events: none;
        z-index: 9999;
    }

    .page-frame::before {
        content: "";
        position: absolute;
        inset: 7px;
        border: 1px solid rgba(74, 141, 255, 0.28);
        border-radius: 13px;
    }

    .page-frame::after {
        content: "";
        position: absolute;
        inset: 15px;
        border: 1px solid rgba(80, 217, 243, 0.10);
        border-radius: 9px;
    }

    /* Small upper corner accents */
    .corner-accent {
        position: fixed;
        top: 18px;
        width: 78px;
        height: 78px;
        pointer-events: none;
        z-index: 10000;
        opacity: 0.9;
    }

    .corner-accent.left {
        left: 18px;
    }

    .corner-accent.right {
        right: 18px;
        transform: scaleX(-1);
    }

    .corner-accent::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 64px;
        height: 64px;
        border-top: 3px solid #50d9f3;
        border-left: 3px solid #4a8dff;
        border-top-left-radius: 11px;
        box-shadow:
            8px 8px 0 -6px #50d9f3,
            16px 16px 0 -13px #4a8dff,
            24px 24px 0 -20px #50d9f3;
    }

    .corner-accent::after {
        content: "";
        position: absolute;
        top: 8px;
        left: 58px;
        width: 7px;
        height: 7px;
        background: #50d9f3;
        border: 1px solid #d8fbff;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(80, 217, 243, 0.85);
    }

    /* --------------------------------------------------
       Hero
    -------------------------------------------------- */
    .hero-kicker {
        color: #50d9f3;
        text-align: center;
        font-size: 0.75rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 0.25rem;
        margin-bottom: 0.65rem;
    }

    .hero-title {
        text-align: center;
        margin: 0 auto 0.4rem auto;
    }

    .hero-line {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        line-height: 0.98;
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
        font-size: 0.95rem;
        line-height: 1.35;
        max-width: 720px;
        margin: 0.75rem auto 1rem auto;
    }

    /* --------------------------------------------------
       Purpose card
    -------------------------------------------------- */
    .purpose-card-title {
        font-family: 'Playfair Display', serif;
        color: #f7f3ee;
        text-align: center;
        font-size: 2rem;
        line-height: 1.1;
        margin-bottom: 0.35rem;
    }

    .purpose-card-subtitle {
        color: #9de8f6;
        text-align: center;
        font-size: 0.92rem;
        margin-bottom: 1rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                rgba(28, 38, 112, 0.96),
                rgba(15, 22, 72, 0.98)
            );
        border: 1px solid rgba(80, 217, 243, 0.78) !important;
        border-radius: 22px !important;
        box-shadow:
            inset 0 0 0 3px rgba(74, 141, 255, 0.10),
            inset 0 0 28px rgba(80, 217, 243, 0.08),
            0 0 35px rgba(80, 217, 243, 0.18);
        padding: 1.1rem 1.2rem 1.25rem 1.2rem;
    }

    /* --------------------------------------------------
       Buttons
    -------------------------------------------------- */
    div[data-testid="stButton"] > button {
        width: 100%;
        min-height: 3.2rem;
        border-radius: 14px;
        border: 1px solid rgba(80, 217, 243, 0.75);
        background:
            linear-gradient(
                145deg,
                rgba(31, 43, 128, 0.98),
                rgba(20, 29, 88, 0.98)
            );
        color: #f7f3ee;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
        box-shadow:
            inset 0 0 0 1px rgba(74, 141, 255, 0.14),
            0 4px 14px rgba(0, 0, 0, 0.20);
    }

    div[data-testid="stButton"] > button:hover {
        color: #ffffff;
        border-color: #50d9f3;
        background:
            linear-gradient(
                145deg,
                rgba(65, 102, 228, 0.98),
                rgba(34, 67, 170, 0.98)
            );
        box-shadow:
            0 0 18px rgba(80, 217, 243, 0.35),
            inset 0 0 0 1px rgba(80, 217, 243, 0.25);
        transform: translateY(-2px);
    }

    div[data-testid="stButton"] > button:focus {
        color: #ffffff;
        border-color: #50d9f3;
        box-shadow:
            0 0 0 2px rgba(80, 217, 243, 0.24),
            0 0 18px rgba(80, 217, 243, 0.28);
    }

    /* --------------------------------------------------
       Selected focus row
    -------------------------------------------------- */
    .focus-display {
        display: flex;
        align-items: center;
        min-height: 3.2rem;
        font-family: 'Inter', sans-serif;
        font-size: 1.18rem;
        font-weight: 800;
        letter-spacing: 0.01em;
    }

    .focus-label {
        color: #4a8dff;
    }

    .focus-value {
        color: #50d9f3;
        margin-left: 0.35rem;
    }

    /* --------------------------------------------------
       Form controls
    -------------------------------------------------- */
    h1,
    h2,
    h3 {
        font-family: 'Inter', sans-serif;
        color: #50d9f3;
        letter-spacing: 0.02em;
    }

    p,
    label,
    .stMarkdown {
        color: #f1eef2;
        font-family: 'Inter', sans-serif;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #50d9f3,
            #4a72ff,
            transparent
        );
        margin: 0.8rem 0;
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
        box-shadow:
            0 0 24px rgba(80, 217, 243, 0.12);
    }

    code {
        color: #f7f3ee !important;
        font-family: 'Inter', sans-serif !important;
        white-space: pre-wrap !important;
    }

    .stCaption,
    caption {
        color: #8edff0 !important;
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(80, 217, 243, 0.55);
        border-radius: 14px;
        background-color: rgba(15, 22, 72, 0.35);
    }

    @media (max-width: 700px) {
        .hero-line {
            font-size: 2.25rem;
        }

        .block-container {
            padding-top: 0.75rem;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }

        .page-frame {
            inset: 6px;
            border-radius: 14px;
        }

        .corner-accent {
            width: 52px;
            height: 52px;
            top: 11px;
        }

        .corner-accent.left {
            left: 11px;
        }

        .corner-accent.right {
            right: 11px;
        }

        .corner-accent::before {
            width: 42px;
            height: 42px;
        }

        .corner-accent::after {
            top: 5px;
            left: 37px;
            width: 6px;
            height: 6px;
        }

        .purpose-card-title {
            font-size: 1.6rem;
        }

        .st-key-purpose_selector {
            display: grid !important;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.5rem;
        }

        .st-key-purpose_selector > div[data-testid="stElementContainer"] {
            grid-column: 1 / -1;
        }

        .st-key-purpose_selector > div[data-testid="stLayoutWrapper"],
        .st-key-purpose_selector
            > div[data-testid="stLayoutWrapper"]
            > div[data-testid="stHorizontalBlock"] {
            display: contents;
        }

        .st-key-purpose_selector
            > div[data-testid="stLayoutWrapper"]
            > div[data-testid="stHorizontalBlock"]
            > div[data-testid="stColumn"] {
            min-width: 0 !important;
            width: 100% !important;
        }

        .focus-display {
            font-size: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Frame markup
# --------------------------------------------------
st.markdown(
    """
    <div class="page-frame"></div>
    <div class="corner-accent left"></div>
    <div class="corner-accent right"></div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    '<div class="hero-kicker">FIRST [AI]D FOR YOUR MIND</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-title">
        <div class="hero-line white">Your Mind.</div>
        <div class="hero-line blue">Your Rules.</div>
        <div class="hero-line cyan">In the Age of AI.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-subtitle">
        Build a starter prompt that helps you use AI with reflection,
        source awareness, and collaborative discipline.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


workspace = st.session_state.get("toolkit_workspace")
if workspace is not None:
    render_workspace(workspace)
    st.stop()


# --------------------------------------------------
# First-screen purpose card
# --------------------------------------------------
if st.session_state.session_purpose is None:
    left_space, center_column, right_space = st.columns([1, 4, 1])

    with center_column:
        with st.container(border=True, key="purpose_selector"):
            st.markdown(
                """
                <div class="purpose-card-title">
                    What would you like to do?
                </div>
                <div class="purpose-card-subtitle">
                    Choose one path to begin our AI session.
                </div>
                """,
                unsafe_allow_html=True,
            )

            row_one = st.columns(3)

            with row_one[0]:
                if st.button(
                    "Learn",
                    key="purpose_learn",
                    use_container_width=True,
                ):
                    st.session_state.session_purpose = "Learn"
                    st.rerun()

            with row_one[1]:
                if st.button(
                    "Explore",
                    key="purpose_explore",
                    use_container_width=True,
                ):
                    st.session_state.session_purpose = "Explore"
                    st.rerun()

            with row_one[2]:
                if st.button(
                    "Research",
                    key="purpose_research",
                    use_container_width=True,
                ):
                    st.session_state.session_purpose = "Research"
                    st.rerun()

            row_two = st.columns(3)

            with row_two[0]:
                if st.button(
                    "Create",
                    key="purpose_create",
                    use_container_width=True,
                ):
                    st.session_state.session_purpose = "Create"
                    st.rerun()

            with row_two[1]:
                if st.button(
                    "Decide",
                    key="purpose_decide",
                    use_container_width=True,
                ):
                    st.session_state.session_purpose = "Decide"
                    st.rerun()

            with row_two[2]:
                if st.button(
                    "Solve",
                    key="purpose_solve",
                    use_container_width=True,
                ):
                    st.session_state.session_purpose = "Solve"
                    st.rerun()

    st.stop()


# --------------------------------------------------
# Selected focus and change control
# --------------------------------------------------
focus_left_column, focus_right_column = st.columns(2)

with focus_left_column:
    st.markdown(
        f"""
        <div class="focus-display">
            <span class="focus-label">Our focus:</span>
            <span class="focus-value">
                {st.session_state.session_purpose}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with focus_right_column:
    button_spacer, button_column = st.columns([1.45, 1])

    with button_column:
        if st.button(
            "Change focus",
            key="change_purpose",
            use_container_width=True,
        ):
            st.session_state.session_purpose = None
            st.rerun()


# --------------------------------------------------
# Guided settings
# --------------------------------------------------
left_column, right_column = st.columns(2)

with left_column:
    source_expectation = st.selectbox(
        "How should the AI handle facts?",
        [
            "General explanation is fine",
            "Separate facts from assumptions",
            "Tell me what needs verification",
            "Ask for sources or citations",
            "Show opposing views or missing context",
        ],
    )

with right_column:
    ai_role = st.selectbox(
        "What role should the AI take?",
        [
            "Patient tutor",
            "Critical thinking partner",
            "Research assistant",
            "Creative collaborator",
            "Decision-support analyst",
        ],
    )

left_column, right_column = st.columns(2)

with left_column:
    answer_style = st.selectbox(
        "How should the AI answer?",
        [
            "Simple beginner explanation",
            "Step-by-step overview",
            "One step at a time, wait for me",
            "Balanced pros and cons",
            "Challenge my assumptions",
            "Give me options, but let me decide",
        ],
    )

with right_column:
    response_length = st.selectbox(
        "How detailed should the answer be?",
        [
            "Short and focused",
            "Moderately detailed",
            "Thorough but clear",
        ],
    )


additional_context = st.text_area(
    "Additional context",
    placeholder=(
        "Add anything that may help the AI understand the situation. "
        "You can leave this blank."
    ),
    height=75,
)

user_inquiry = st.text_area(
    "What would you like to explore together?",
    placeholder=(
        "Example: Help me understand how large language models work."
    ),
    height=85,
)


# --------------------------------------------------
# Generated prompt
# --------------------------------------------------
rules = CollaborationRules(
    evidence_expectation=source_expectation,
    ai_role=ai_role,
    answer_style=answer_style,
    response_length=response_length,
)
generated_prompt = build_prompt(
    st.session_state.session_purpose, rules, additional_context, user_inquiry
)


with st.expander("View and copy your starter prompt"):
    st.code(
        generated_prompt,
        language="text",
    )

st.caption(
    "AI is a partner, not a substitute. "
    "You remain responsible for judgment, meaning, and action."
)

render_start(st.session_state.session_purpose, user_inquiry, additional_context, rules)
