# Human-AI Cognitive Toolkit App

A human-centered AI companion designed to help people work with large language models while preserving critical thinking, emotional awareness, creativity, and human decision-making.

The project translates the Human-AI Cognitive Toolkit into an accessible digital experience without replacing the physical cards or changing their underlying philosophy.

The core mindset is **collaborative discipline**:

> Work with AI deliberately, reflectively, and skeptically—without surrendering human judgment.

---

## Current MVP

The current version is a lightweight Streamlit prompt builder.

Users select:

- What they are using AI for
- What role the AI should take
- Relevant human context
- Source and evidence expectations
- Preferred answer style

The app then generates a structured prompt that users can copy and paste into the LLM or chatbot of their choice.

### Current Flow

```text
Choose settings
      ↓
Add human context
      ↓
Generate starter prompt
      ↓
Copy into an LLM
      ↓
Human reviews and interprets the result
```

### Current Technology

- Python
- Streamlit
- GitHub
- Streamlit Community Cloud

---

# Product Principles

The app should:

- Help people think better, not merely faster
- Preserve human interpretive authority
- Distinguish facts, assumptions, opinions, and uncertainty
- Encourage source awareness and verification
- Highlight missing context and blind spots
- Support emotional and cultural awareness
- Avoid presenting AI as an oracle or final decision-maker
- Complement the physical toolkit rather than replace it

---

# Iterative Development Roadmap

The project will grow in controlled stages. Each iteration should be tested before additional complexity is added.

---

## Iteration 1: One-Page Prompt Builder

### Goal

Provide a simple, usable prompt-building experience that nearly fits on one screen and does not overwhelm younger or first-time users.

### Features

- Session-purpose dropdown
- AI-role dropdown
- Human-context text field
- Source-awareness selection
- Answer-style selection
- Copyable generated prompt
- Human judgment reminder

### Tools

- Streamlit
- Python dictionaries and formatted strings
- Custom CSS
- GitHub
- Streamlit Community Cloud

### Status

Current working MVP.

---

## Iteration 2: Personalized User Setup

### Goal

Adjust the experience based on who is using it.

A short introductory sequence may collect:

- Age or learner bracket
- AI experience level
- Reading level
- Purpose of use
- Preferred amount of guidance
- Preferred response length

### Example Profiles

```text
Younger learner
Teen or student
Adult beginner
Educator
Professional
Advanced AI user
```

### What Changes

The app can adjust:

- Vocabulary
- Length of generated prompts
- Number of dropdown choices
- Complexity of instructions
- Amount of explanation
- Reflection questions
- Verification expectations

### Possible Tools

- Streamlit session state
- Python configuration files
- JSON-based user profiles
- Pydantic for validating profile settings

---

## Iteration 3: Before, During, and After AI Sessions

### Goal

Guide users through the toolkit’s reflective process instead of only generating a starting prompt.

### Before AI

- What am I trying to accomplish?
- What do I already believe or understand?
- What might I be asking AI to replace?
- What emotions, assumptions, or values am I bringing?

### During AI

- Is the answer clarifying or narrowing my thinking?
- Is the AI sounding confident without evidence?
- What claims require verification?
- What context may be missing?

### After AI

- What changed in my understanding?
- Which parts do I agree or disagree with?
- What still needs checking?
- What is my final human interpretation or decision?

### Possible Tools

- Streamlit tabs or multi-step forms
- Streamlit session state
- Local JSON session records
- Export to Markdown or PDF
- Optional card-category selection

---

## Iteration 4: Card-Aligned Guided Experience

### Goal

Connect the application more directly to the toolkit components.

### Card Families

- AI Reality Check Cards
- Epistemic Literacy Cards
- Reflective Question Strips
- Fact-Check Checklist Cards
- Emotional Anchor Reminders
- Discrepancy Comparison tools
- Cognitive-friction activities
- Emergency practice guides

The application may surface a small number of relevant reminders rather than digitizing every card at once.

### Possible Tools

- Structured JSON card library
- Tagging and filtering
- Rule-based card selection
- Searchable card categories
- Licensed image assets where appropriate

---

## Iteration 5: Saved Sessions and Reflection Diary

### Goal

Allow users to save their AI-use process and reflect on how their thinking changed.

### Possible Features

- Save generated prompts
- Record the AI response
- Capture the user’s original thinking
- Compare human and AI contributions
- Record unresolved questions
- Export a reflection summary
- Track repeated patterns over time

### Possible Tools

- SQLite for an early prototype
- PostgreSQL or Supabase for hosted storage
- Supabase Auth, Clerk, or Auth0 for login
- Pandas for exports and summaries
- ReportLab or another document library for PDF reports

### Privacy Principle

The system should collect the minimum amount of data necessary and clearly explain:

- What is stored
- Why it is stored
- Who can access it
- How it can be deleted

---

## Iteration 6: Custom GPT Companion

### Goal

Create a version that users can access directly inside ChatGPT.

The Custom GPT could guide users through:

- Starting an AI session
- Reviewing an AI answer
- Fact-checking claims
- Reflecting on emotional responses
- Identifying missing context
- Preserving human interpretive authority

### Possible Tools

- Custom GPT instructions
- Conversation starters
- Approved toolkit knowledge files
- GPT Actions later, if external services are needed

This should follow the tested toolkit flow rather than becoming a generic chatbot wrapper.

---

## Iteration 7: Built-In LLM Assistance

### Goal

Allow users to interact with an AI model directly inside the application instead of copying and pasting prompts elsewhere.

### Possible Flow

```text
User completes guided setup
        ↓
Application builds structured prompt
        ↓
Backend sends prompt to an LLM API
        ↓
Model returns structured response
        ↓
Application displays:
- Answer
- Assumptions
- Uncertainty
- Source requirements
- Reality check
- Your-turn reflection
```

### Possible Tools

- OpenAI API or another approved model provider
- FastAPI backend
- Pydantic structured outputs
- Streamlit frontend
- Environment variables for API keys
- Rate limiting
- Usage logging
- Model-response evaluation

### Security Requirements

- Never place API keys directly in source code
- Use environment variables or managed secrets
- Do not commit `.env` files
- Minimize stored user prompts and responses
- Add clear warnings for sensitive or high-stakes use

---

## Iteration 8: Premium User Features

### Goal

Support advanced users, educators, teams, or organizations while keeping the basic toolkit accessible.

### Possible Premium Features

- Direct model access inside the app
- Longer or more advanced sessions
- Saved history
- Reflection reports
- Educator dashboards
- Classroom assignments
- Team workspaces
- Custom prompt frameworks
- Organization-specific guidance
- Multiple model choices
- Advanced source-verification workflows

### Possible Tools

- Stripe for subscriptions and payments
- Supabase or PostgreSQL
- User authentication
- Usage quotas
- Role-based access control
- FastAPI backend
- Hosted deployment through services such as Render, Railway, Azure, AWS, or Google Cloud

Premium access should pay for infrastructure and advanced features, not remove the human-centered safeguards.

---

## Iteration 9: Cultural Context and Bias Review

### Goal

Help users recognize when AI output may be culturally narrow, regionally incomplete, historically flattened, or based primarily on dominant perspectives.

This should not be marketed as a perfect mathematical removal of bias.

AI bias cannot be eliminated through a single equation. Cultural meaning is contextual, contested, and dependent on lived human experience.

Instead, the application may use a transparent **Cultural Context Review Score** as a prompting and reflection aid.

### Conceptual Framework

```text
Cultural Context Review Score =
    Source Diversity
  + Regional Relevance
  + Historical Context
  + Opposing Perspective Coverage
  + Uncertainty Disclosure
  + Human Cultural Review
```

A weighted prototype could later be represented as:

```text
CCRS =
w1(Source Diversity)
+ w2(Regional Relevance)
+ w3(Historical Context)
+ w4(Perspective Coverage)
+ w5(Uncertainty Disclosure)
+ w6(Human Review)
```

The weights would depend on the use case and should never be presented as universal truth.

### Possible Checks

- Which cultures or regions are represented?
- Which perspectives are absent?
- Are sources concentrated in one geography or language?
- Is the answer treating one cultural norm as universal?
- Is historical context missing?
- Are marginalized or local perspectives included?
- Does the user have relevant lived experience that the model lacks?
- Should a cultural subject-matter expert review the answer?

### Possible Tools

- Structured metadata for source geography and language
- Source-diversity analysis
- Retrieval from curated cultural or regional sources
- Human review workflows
- Bias and representation evaluation datasets
- Multilingual embeddings
- RAG with approved cultural knowledge collections
- Transparent scoring rules
- Model-evaluation dashboards

The final authority remains human.

---

## Iteration 10: Educator and Organization Platform

### Goal

Provide structured AI-literacy learning for schools, educators, workplaces, and community organizations.

### Possible Features

- Teacher-created exercises
- Student reflection assignments
- Prompt revision history
- Fact-check activities
- Classroom discussion prompts
- Learner progress tracking
- Organization-approved AI-use frameworks
- Human-review requirements
- Exportable reports
- Privacy-aware administrative controls

### Possible Tools

- React or Next.js frontend if the application outgrows Streamlit
- FastAPI backend
- PostgreSQL
- Learning-management-system integrations
- OAuth or school identity providers
- Role-based permissions
- Analytics dashboards
- Containerized deployment with Docker

---

# Proposed Architecture Evolution

```text
Phase 1
Streamlit-only prompt builder

Phase 2
Streamlit + configuration profiles

Phase 3
Streamlit + session state + exports

Phase 4
Streamlit + database + authentication

Phase 5
Streamlit frontend + FastAPI backend + LLM API

Phase 6
Subscriptions + usage controls + saved sessions

Phase 7
Custom GPT + external actions

Phase 8
Full web platform for educators and organizations
```

---

# Development Discipline

Each phase should follow this loop:

```text
Build one small feature
        ↓
Test with real users
        ↓
Compare behavior with toolkit principles
        ↓
Document pushback and tradeoffs
        ↓
Refine wording and interaction
        ↓
Only then add complexity
```

The project should avoid:

- Unnecessary early infrastructure
- Overly complicated onboarding
- Pretending AI output is automatically trustworthy
- Replacing reflection with automation
- Treating cultural bias as a solved equation
- Turning the toolkit into a generic chatbot
- Changing the original toolkit philosophy to fit the software

---

# Implementation Diary

The project maintains an implementation diary documenting:

- How the digital product was created
- How each feature maps to the original cards
- Where scope was reduced
- Where technical pushback occurred
- Where research or evidence was requested
- Where output differences were tested
- How first-time users responded
- How collaborative discipline shaped the build

This provides a record of how the technical implementation remained aligned with the original human-centered vision.

---

# Collaboration

The toolkit philosophy, message, and card system guide the product.

The technical implementation translates those ideas into a usable application while preserving their intent.

The shared operating principle is:

> Respect the message. Test the implementation. Preserve human agency.

---

# Current Status

```text
Working Streamlit MVP
GitHub repository configured
Initial visual branding applied
Prompt-generation flow working
Private prototype deployment in progress
```

---

# Near-Term Next Steps

1. Deploy the current Streamlit prototype.
2. Test the one-page experience with collaborators.
3. Refine dropdown wording.
4. Add clearer answer-length choices.
5. Split step-by-step response styles.
6. Add required Reality Check and Your Turn sections.
7. Design the age and experience onboarding flow.
8. Continue documenting decisions in the implementation diary.