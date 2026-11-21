import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import toolkit_chat as chat
from toolkit_memory import Brief, Decision, Evidence, Option, export_markdown
from tests import nonprofit_scenario as scenario

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_approval_and_export_preserve_authority_and_relationships():
    initial = Brief(project=scenario.new_project(), focus="Research")
    approved = initial.approve_review(
        for_brief_id=initial.brief_id, move_to_decide=True, **scenario.approved_notes()
    )
    assert approved.project == initial.project
    assert approved.focus == "Decide"
    assert approved.parent_brief_id == initial.brief_id
    assert approved.version == 2
    assert not approved.decisions
    assert approved.evidence[0].judgment == "Accepted by user"
    assert approved.evidence[0].verification == "Unverified"
    assert approved.evidence[2].source_reference is None
    assert approved.options[1].status == "Rejected by user"

    with pytest.raises(ValueError, match="project changed"):
        approved.approve_review(
            for_brief_id=initial.brief_id, move_to_decide=True, **scenario.approved_notes()
        )
    with pytest.raises(ValueError, match="rejected alternatives"):
        approved.confirm_decision(
            Decision(
                chosen_option=scenario.PILOT, rationale="Limit the trial.",
                rejected_option_ids=(approved.options[0].option_id,),
            )
        )
    with pytest.raises(ValueError, match="source reference"):
        Evidence(claim=scenario.UNSUPPORTED, verification="Verified by user")

    decision = Decision(
        chosen_option=scenario.PILOT,
        rationale="A small trial tests the FAQ coverage before committing.",
        evidence_ids=(approved.evidence[0].evidence_id,),
        rejected_option_ids=(approved.options[1].option_id,),
    )
    prior = approved.confirm_decision(decision)
    updated = prior.confirm_decision(
        Decision(
            chosen_option="Defer the trial.",
            rationale="We need retention controls confirmed first.",
            supersedes_decision_id=decision.decision_id,
        )
    )
    assert updated.decisions[0] == decision
    markdown = export_markdown(updated)
    assert "Superseded decision" in markdown and "Current decision" in markdown
    assert "## Reality Check" in markdown and "## Your Turn" in markdown
    snapshot = markdown.split("\n```json\n", 1)[1].split("\n```", 1)[0]
    assert Brief.model_validate_json(snapshot) == updated
    assert json.loads(snapshot)["decisions"][0]["evidence_ids"] == [str(approved.evidence[0].evidence_id)]


def test_repeated_notes_preserve_record_ids_and_rejected_status():
    brief = Brief(project=scenario.new_project(), focus="Research")
    first = brief.approve_review(
        for_brief_id=brief.brief_id, move_to_decide=False, **scenario.approved_notes()
    )
    revised = first.approve_review(
        for_brief_id=first.brief_id,
        move_to_decide=True,
        evidence=(Evidence(
            claim=scenario.FAQ_FINDING, source_reference=scenario.FAQ_SOURCE,
            source_support="Supports claim", verification="Verified by user",
        ),),
        options=(Option(description=scenario.REJECTED.upper(), status="Brainstormed"),),
        questions=first.open_questions,
        reality_check=scenario.REALITY_CHECK,
    )
    assert len(revised.evidence) == 3
    assert revised.evidence[0].evidence_id == first.evidence[0].evidence_id
    assert revised.evidence[0].verification == "Verified by user"
    assert revised.options == first.options
    assert revised.open_questions == first.open_questions


def test_existing_prompt_builder_without_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app = AppTest.from_file(str(APP)).run()
    assert len(app.button) == 6
    app.button(key="purpose_research").click().run()
    assert "Reality Check" in app.code[0].value
    assert "Your Turn" in app.code[0].value
    assert any("OPENAI_API_KEY" in item.value for item in app.info)
    app.button(key="change_purpose").click().run()
    assert len(app.button) == 6 and not app.exception


def test_streamlit_nonprofit_research_to_decide(monkeypatch):
    requests = []

    def reply(_key, _model, instructions, turns):
        requests.append((instructions, turns))
        return chat.ChatReply(
            answer="Here is where the research stands.",
            reality_check=scenario.REALITY_CHECK,
            your_turn="What should we verify?",
            requests_decide=turns[-1].content == scenario.SWITCH,
        )

    def draft(_key, _model, turns):
        assert turns[-2].content == scenario.SWITCH
        return chat.ReviewDraft(
            evidence=[
                chat.EvidenceDraft(claim=scenario.FAQ_FINDING, source_reference=scenario.FAQ_SOURCE, notes=""),
                chat.EvidenceDraft(claim=scenario.ROTA_FINDING, source_reference=scenario.ROTA_SOURCE, notes=""),
                chat.EvidenceDraft(claim=scenario.UNSUPPORTED, source_reference="Made-up citation", notes=""),
            ],
            options=[
                chat.OptionDraft(option=scenario.PILOT, explicitly_rejected=False, reason="Brainstormed"),
                chat.OptionDraft(option=scenario.REJECTED, explicitly_rejected=True, reason="Rejected by user"),
            ],
            open_questions=[scenario.QUESTION],
            reality_check=scenario.REALITY_CHECK,
        )

    monkeypatch.setattr(chat, "reply", reply)
    monkeypatch.setattr(chat, "draft_review", draft)
    app = AppTest.from_file(str(APP))
    app.secrets["OPENAI_API_KEY"] = "testing-placeholder"
    app.run()
    app.button(key="purpose_research").click().run()
    app.selectbox[0].select("Separate facts from assumptions")
    app.text_area[1].input(scenario.GOAL)
    app.text_area(key="toolkit_initial_constraints").input(scenario.CONSTRAINT)
    app.button(key="toolkit_start").click().run()
    first = app.session_state.toolkit_workspace.brief

    app.chat_input(key="toolkit_chat").set_value(scenario.MATERIAL).run()
    app.chat_input(key="toolkit_chat").set_value(scenario.SWITCH).run()
    assert not app.exception
    assert "Separate facts from assumptions" in requests[0][0]
    assert "Reality Check" in requests[0][0]
    assert app.session_state.toolkit_workspace.brief == first
    review = f"review_{first.brief_id}"
    assert app.text_input(key=f"{review}_evidence_2_source").value == ""
    app.selectbox(key=f"{review}_evidence_0_judgment").select("Accepted by user")
    for index in range(3):
        app.checkbox(key=f"{review}_evidence_{index}_include").check()
    for index in range(2):
        app.checkbox(key=f"{review}_option_{index}_include").check()
    app.checkbox(key=f"{review}_include_question_0").check()
    next(button for button in app.button if button.label == "Approve and switch to Decide").click().run()
    approved = app.session_state.toolkit_workspace.brief
    assert not app.exception
    assert approved.focus == "Decide" and approved.project == first.project
    assert approved.evidence[0].source_reference == scenario.FAQ_SOURCE
    assert approved.evidence[0].judgment == "Accepted by user"
    assert approved.evidence[0].verification == "Unverified"
    assert approved.evidence[1].source_reference == scenario.ROTA_SOURCE
    assert approved.evidence[2].source_reference is None
    assert approved.open_questions[0].question == scenario.QUESTION
    assert approved.options[1].status == "Rejected by user"
    assert not approved.decisions
    assert app.get("download_button")[0].proto.label == "Download SESSION_BRIEF.md"

    app.chat_input(key="toolkit_chat").set_value("What should I consider first?").run()
    turns = requests[-1][1]
    assert len(turns) == 2 and "Decide" in turns[0].content
    assert scenario.FAQ_SOURCE in turns[0].content and scenario.SWITCH not in turns[0].content

    next(widget for widget in app.text_input if widget.label == "Your decision").input(scenario.PILOT)
    next(widget for widget in app.text_area if widget.label == "Why did you choose it?").input("Pilot publicly documented FAQs.")
    next(button for button in app.button if button.label == "Confirm my decision").click().run()
    assert not app.exception
    assert app.session_state.toolkit_workspace.brief.decisions[0].human_confirmed


def test_failed_chat_can_retry_without_duplicate_turns(monkeypatch):
    def fail(*args):
        raise chat.ChatError("Temporarily unavailable.")

    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setattr(chat, "reply", fail)
    app = AppTest.from_file(str(APP)).run()
    app.button(key="purpose_research").click().run()
    app.text_area[1].input(scenario.GOAL)
    app.button(key="toolkit_start").click().run()
    app.chat_input(key="toolkit_chat").set_value("Help me start.").run()
    assert app.error[0].value == "Temporarily unavailable."
    workspace = app.session_state.toolkit_workspace
    assert not workspace.turns
    assert workspace.unsent == "Help me start."
    monkeypatch.setattr(
        chat, "reply",
        lambda *args: chat.ChatReply(
            answer="Start with the existing FAQs.",
            reality_check="Coverage is uncertain.",
            your_turn="Which FAQs should we check?",
            requests_decide=False,
        ),
    )
    app.button(key="toolkit_retry").click().run()
    assert not app.error and not app.exception
    assert len(workspace.turns) == 2 and workspace.unsent is None


def test_responses_sdk_parses_structured_reply(monkeypatch):
    import httpx
    from openai import OpenAI

    response_body = {
        "answer": "Assess FAQ coverage first.",
        "reality_check": "Staff capacity is limited.",
        "your_turn": "Which FAQs matter most?",
        "requests_decide": False,
    }

    def handle(request):
        payload = json.loads(request.content)
        assert request.url.path == "/v1/responses"
        assert payload["model"] == chat.DEFAULT_MODEL
        assert payload["store"] is False
        assert payload["input"][0]["role"] == "user"
        output_format = payload["text"]["format"]
        assert output_format["type"] == "json_schema"
        assert output_format["strict"] is True
        assert set(output_format["schema"]["required"]) == set(response_body)
        return httpx.Response(200, json={
            "id": "resp_test",
            "object": "response",
            "status": "completed",
            "created_at": 0,
            "model": chat.DEFAULT_MODEL,
            "output": [{
                "id": "msg_test", "type": "message", "role": "assistant", "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps(response_body), "annotations": []}],
            }],
        })

    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(
        chat, "OpenAI", lambda **kwargs: OpenAI(http_client=httpx.Client(transport=transport), **kwargs)
    )
    output = chat.reply(
        "test-key",
        chat.DEFAULT_MODEL,
        "Include a Reality Check.",
        [chat.Turn(role="user", content=scenario.MATERIAL)],
    )
    assert output.model_dump() == response_body
    assert "**Reality Check**" in output.as_markdown()


def test_responses_sdk_sends_review_task_after_chat_transcript(monkeypatch):
    import httpx
    from openai import OpenAI

    response_body = {
        "evidence": [{"claim": scenario.UNSUPPORTED, "source_reference": None, "notes": "Unsupported"}],
        "options": [{"option": scenario.REJECTED, "explicitly_rejected": True, "reason": "User declined"}],
        "open_questions": [scenario.QUESTION],
        "reality_check": scenario.REALITY_CHECK,
    }

    def handle(request):
        payload = json.loads(request.content)
        assert [turn["role"] for turn in payload["input"]] == ["user", "assistant", "user"]
        assert "structured handoff proposal" in payload["input"][-1]["content"]
        schema = payload["text"]["format"]["schema"]
        assert set(schema["required"]) == set(response_body)
        assert set(schema["$defs"]["EvidenceDraft"]["required"]) == {
            "claim", "source_reference", "notes"
        }
        return httpx.Response(200, json={
            "id": "resp_review_test",
            "object": "response",
            "status": "completed",
            "created_at": 0,
            "model": chat.DEFAULT_MODEL,
            "output": [{
                "id": "msg_review_test", "type": "message", "role": "assistant", "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps(response_body), "annotations": []}],
            }],
        })

    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(
        chat, "OpenAI", lambda **kwargs: OpenAI(http_client=httpx.Client(transport=transport), **kwargs)
    )
    draft = chat.draft_review(
        "test-key",
        chat.DEFAULT_MODEL,
        [
            chat.Turn(role="user", content=scenario.MATERIAL),
            chat.Turn(role="assistant", content="I’ll prepare the handoff."),
        ],
    )
    assert draft.model_dump() == response_body


def test_review_api_error_logs_status_and_request_id_without_body(monkeypatch, caplog):
    import httpx
    from openai import OpenAI

    def handle(request):
        return httpx.Response(
            400,
            headers={"x-request-id": "req_test_review"},
            json={"error": {"message": "Private API error body"}},
        )

    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(
        chat, "OpenAI", lambda **kwargs: OpenAI(http_client=httpx.Client(transport=transport), **kwargs)
    )
    with pytest.raises(chat.ChatError, match="OpenAI returned HTTP 400"):
        chat.draft_review(
            "test-key",
            chat.DEFAULT_MODEL,
            [chat.Turn(role="user", content=scenario.MATERIAL)],
        )
    assert "ReviewDraft returned HTTP 400 (request ID req_test_review)" in caplog.text
    assert "Private API error body" not in caplog.text
