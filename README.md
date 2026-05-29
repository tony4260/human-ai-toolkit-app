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