"""Capture live ordinary, toolkit, and fresh-chat outputs for the same nonprofit case."""

import os

from openai import APIError, OpenAI

import toolkit_chat as chat
from toolkit_memory import Brief, export_markdown
from tests import nonprofit_scenario as scenario

RUBRIC = (
    "Preserves the adoption goal and the no-personal-data constraint.",
    "Cites both named source excerpts and accurately states what they support.",
    "Labels the workload reduction estimate as unsupported.",
    "Keeps the public FAQ pilot brainstormed, rejects case-history access, and reports no confirmed decision.",
    "Asks the human to make or confirm a decision.",
    "Identifies unanswered questions about retention controls and escalation.",
)


def ordinary_reply(client: OpenAI, model: str, turns: list[chat.Turn]) -> str:
    response = client.responses.create(
        model=model,
        input=[{"role": turn.role, "content": turn.content} for turn in turns],
        max_output_tokens=4000,
        store=False,
    )
    if not response.output_text.strip():
        raise chat.ChatError("Ordinary conversation returned no text.")
    return response.output_text


def show(title: str, content: str):
    print(f"\n## {title}\n\n{content}", flush=True)


def run(api_key: str, model: str):
    research = chat.Turn(role="user", content=scenario.MATERIAL)
    switch = chat.Turn(role="user", content=scenario.SWITCH)
    continuation = chat.Turn(role="user", content=scenario.CONTINUE)

    with OpenAI(api_key=api_key, timeout=30.0, max_retries=0) as client:
        ordinary_turns = []
        for title, turn in (
            ("A · Research", research), ("A · Switch", switch), ("A · Decide", continuation)
        ):
            ordinary_turns.append(turn)
            answer = ordinary_reply(client, model, ordinary_turns)
            show(title, answer)
            ordinary_turns.append(chat.Turn(role="assistant", content=answer))

        brief = Brief(project=scenario.new_project(), focus="Research")

        toolkit_turns = []
        for title, turn in (("B · Research", research), ("B · Switch", switch)):
            toolkit_turns.append(turn)
            response = chat.reply_for_brief(api_key, model, brief, toolkit_turns)
            show(title, response.as_markdown())
            toolkit_turns.append(chat.Turn(role="assistant", content=response.as_markdown()))
        show("B · Switch detected", str(response.requests_decide))

        draft = chat.draft_review(api_key, model, [chat.project_context(brief), *toolkit_turns])
        show("B · Actual handoff proposal", draft.model_dump_json(indent=2))
        brief = brief.approve_review(
            for_brief_id=brief.brief_id, move_to_decide=True, **scenario.approved_notes()
        )
        reviewed_reply = chat.reply_for_brief(api_key, model, brief, [continuation])
        show("B · Decide after scripted human review", reviewed_reply.as_markdown())
        snapshot = export_markdown(brief)
        show("Approved brief", snapshot)
        show(
            "Fresh chat · Brief and continuation request only",
            ordinary_reply(client, model, [chat.Turn(role="user", content=snapshot), continuation]),
        )


if __name__ == "__main__":
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise SystemExit("Live comparison requires OPENAI_API_KEY in the environment.")
    model = os.environ.get("OPENAI_MODEL", chat.DEFAULT_MODEL)
    print(f"# Nonprofit comparison using {model}\n\nScore each output against the same criteria.")
    for item in RUBRIC:
        print(f"- {item}")
    print(
        "\nUse A · Decide, B · Decide, and Fresh chat for the same rubric. "
        "Record specific errors or omissions. Separately inspect the actual handoff proposal "
        "for missed findings, invented references, or changed statuses. The fixed input to human "
        "approval gives every run the same opportunity for human correction.",
        flush=True,
    )
    try:
        run(key, model)
    except (APIError, chat.ChatError) as error:
        show("Run stopped", type(error).__name__)
        raise SystemExit(1) from None
