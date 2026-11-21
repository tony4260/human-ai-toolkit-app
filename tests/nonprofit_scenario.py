"""Synthetic source packet and predefined human annotations for a repeatable comparison."""

from toolkit_memory import CollaborationRules, Evidence, OpenQuestion, Option, Project

GOAL = "Decide whether a small nonprofit should adopt an AI chatbot to answer public questions."
CONSTRAINT = "The chatbot must never collect or retain visitors' personal data."
FAQ_SOURCE = "Nonprofit FAQ inventory audit, §2"
ROTA_SOURCE = "Nonprofit support rota, November pilot"
FAQ_FINDING = "38 of 50 recent public questions matched an existing public FAQ."
ROTA_FINDING = "Two staff members are available to review escalated questions twice each weekday."
UNSUPPORTED = "The chatbot would cut public support workload in half."
PILOT = "Pilot a chatbot limited to the public FAQ."
REJECTED = "Let the chatbot answer eligibility questions using visitor case histories."
QUESTION = "Can the vendor disable message retention and route unanswered questions to staff?"
REALITY_CHECK = "Verify retention controls and human escalation. Workload savings remain unverified."
MATERIAL = f"""Use this synthetic project packet for our research.

Goal: {GOAL}
Confirmed constraint: {CONSTRAINT}
Source excerpt from {FAQ_SOURCE}: "{FAQ_FINDING}"
Source excerpt from {ROTA_SOURCE}: "{ROTA_FINDING}"
Unsupported estimate someone floated: {UNSUPPORTED}
Brainstormed option only: {PILOT}
I explicitly rejected this proposal: {REJECTED}
Still to verify: {QUESTION}
I have made no adoption decision. Summarize what the research supports and what remains open.
"""
SWITCH = "We're done researching for now. Help me decide."
CONTINUE = (
    "For the next step, state the original goal and current focus, carry forward the constraint, "
    "cite the two source-supported findings, distinguish the unsupported claim and options, "
    "report any confirmed decisions, and ask what I want to verify or decide."
)


def new_project() -> Project:
    return Project(
        goal=GOAL,
        purpose="Research",
        constraints=(CONSTRAINT,),
        collaboration=CollaborationRules(
            evidence_expectation="Separate facts from assumptions",
            ai_role="Research assistant",
            answer_style="Balanced pros and cons",
            response_length="Short and focused",
        ),
    )


def approved_notes() -> dict:
    # Fixed annotations represent the human review step in the controlled comparison.
    return dict(
        evidence=(
            Evidence(
                claim=FAQ_FINDING,
                source_reference=FAQ_SOURCE,
                source_support="Supports claim",
                judgment="Accepted by user",
                interpretation="I accept this excerpt as relevant to the pilot.",
            ),
            Evidence(claim=ROTA_FINDING, source_reference=ROTA_SOURCE, source_support="Supports claim"),
            Evidence(claim=UNSUPPORTED),
        ),
        options=(
            Option(description=PILOT, status="Brainstormed"),
            Option(description=REJECTED, status="Rejected by user"),
        ),
        questions=(OpenQuestion(question=QUESTION),),
        reality_check=REALITY_CHECK,
    )
