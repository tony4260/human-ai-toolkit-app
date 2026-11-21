# Human-AI Toolkit App

A small Streamlit prototype for the Human-AI Cognitive Toolkit.

This app helps users start an AI session with more reflection, source awareness, and collaborative discipline. It generates a copy/paste starter prompt that encourages the user to stay involved in the thinking process instead of letting the AI do all the work.

## Current Features

- Dropdown-based session setup
- AI role/personality selection
- Human context field
- Source and uncertainty expectation selection
- Answer style selection
- Generated starter prompt for use with an LLM

## Project Goal

The goal is not to replace human thinking.

The goal is to help people use AI as a partner while preserving:

- Human agency
- Critical thinking
- Reflection
- Source awareness
- Interpretive authority
- Collaborative discipline

## Run Locally

Clone the repo, then from the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## V1.1 in-app conversation

Set `OPENAI_API_KEY` in your shell environment or as a top-level Streamlit secret.
The prompt builder is available without a key. The conversation uses the OpenAI
Responses API and defaults to `gpt-5-mini`. Set `OPENAI_MODEL` to use another
model that supports Responses API Structured Outputs.

1. Select **Research** and set your evidence and collaboration preferences.
2. Enter the project goal and any context, then open **Start an in-app conversation**.
   Enter any established constraints before starting.
3. Research in chat. Ask to move to Decide or select **Prepare handoff to Decide**.
4. Review the proposed notes, choose which to include, and approve the switch.
   The Decide conversation uses the approved record. Use **Record a human decision**
   to confirm a choice or supersede an earlier decision.
5. Download **SESSION_BRIEF.md** before closing the session. To continue elsewhere,
   provide that brief to a fresh chat along with your next question.

A source reference, a human verification, and the user's acceptance are recorded
separately. Session records live in Streamlit session memory. The Markdown brief
contains a readable summary and a JSON snapshot with the same stable record IDs.

### Checks

```bash
python -m pip install pytest
python -m pytest -q
```

With an API key in the environment, run the live comparison from the repository root.

```bash
python -m tests.compare_nonprofit > nonprofit-comparison.md
```

The exercise uses the same synthetic source packet and model in both conditions.
It captures the ordinary conversation, the toolkit's actual proposal, the Decide
response following a scripted human review, and a fresh response using only the
brief and continuation request. Apply the printed rubric to each output and
record specific failures.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full 10-stage product and architecture plan.
