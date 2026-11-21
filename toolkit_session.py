"""Streamlit conversation and review controls."""

import os
from dataclasses import dataclass, field
from typing import get_args

import streamlit as st
from pydantic import ValidationError

import toolkit_chat as chat
from toolkit_memory import (
    Brief,
    CollaborationRules,
    Decision,
    Evidence,
    OpenQuestion,
    Option,
    Project,
    export_markdown,
)


@dataclass
class PendingReview:
    brief: Brief
    draft: chat.ReviewDraft
    move_to_decide: bool


@dataclass
class Workspace:
    brief: Brief
    turns: list[chat.Turn] = field(default_factory=list)
    phase_start: int = 0
    reviewed_through: int = 0
    pending_review: PendingReview | None = None
    wants_decide: bool = False
    unsent: str | None = None


def _setting(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value.strip() or None
    try:
        value = st.secrets.get(name)
    except FileNotFoundError:
        return None
    return (value.strip() or None) if isinstance(value, str) else None


def _lines(value: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in value.splitlines() if line.strip())


def _validation_error(error: ValueError):
    if isinstance(error, ValidationError):
        for item in error.errors(include_url=False):
            where = " → ".join(map(str, item["loc"]))
            st.error(f"{where} · {item['msg']}" if where else item["msg"])
    else:
        st.error(str(error))


def render_start(purpose: str, goal: str, context: str, rules: CollaborationRules):
    with st.expander("Start an in-app conversation"):
        if not _setting("OPENAI_API_KEY"):
            st.info("Set OPENAI_API_KEY in the environment or Streamlit secrets to use in-app chat.")
            return
        st.caption("Chat sends your project context and messages to OpenAI. Download your brief to keep a copy.")
        constraints = st.text_area(
            "Established constraints (one per line)", key="toolkit_initial_constraints"
        )
        if st.button("Start conversation", key="toolkit_start"):
            if not goal.strip():
                st.warning("Enter your project goal in “What would you like to explore together?”")
                return
            project = Project(
                goal=goal,
                purpose=purpose,
                constraints=_lines(constraints),
                collaboration=rules,
                additional_context=context,
            )
            st.session_state.toolkit_workspace = Workspace(Brief(project=project, focus=purpose))
            st.rerun()


def _review_field_options(field_name: str) -> tuple[str, ...]:
    # The UI and the validated record share the same allowed values.
    return get_args(Evidence.model_fields[field_name].annotation)


def _render_review(workspace: Workspace):
    pending = workspace.pending_review
    draft = pending.draft
    project = pending.brief.project
    unreviewed = workspace.turns[workspace.reviewed_through:]
    user_messages = [turn.content for turn in unreviewed if turn.role == "user"]
    st.subheader("Review Research → Decide" if pending.move_to_decide else "Review session notes")
    st.text(f"Goal · {project.goal}")
    st.text(f"Original purpose · {project.purpose}")
    st.text(f"Focus after approval · {'Decide' if pending.move_to_decide else pending.brief.focus}")
    st.text(f"Evidence expectation · {project.collaboration.evidence_expectation}")
    st.text(f"AI role · {project.collaboration.ai_role}")
    st.text(f"Answer style · {project.collaboration.answer_style}")
    st.text(f"Response detail · {project.collaboration.response_length}")
    st.text("Established constraints · " + (" · ".join(project.constraints) or "None recorded"))
    st.caption("Include the items you want in the brief and record your own judgment where relevant.")
    key = f"review_{pending.brief.brief_id}"
    with st.form(key, enter_to_submit=False):
        evidence_fields = []
        option_fields = []
        question_fields = []
        st.markdown("#### Evidence")
        if not draft.evidence:
            st.caption("No new evidence proposed.")
        manual_evidence = chat.EvidenceDraft(claim="", source_reference=None, notes="")
        for index, item in enumerate([*draft.evidence, manual_evidence]):
            proposed = index < len(draft.evidence)
            prefix = f"{key}_evidence_{index}"
            previous = next(
                (
                    known for known in pending.brief.evidence
                    if known.claim.casefold() == item.claim.strip().casefold()
                    and known.source_reference == item.source_reference
                ),
                None,
            )
            cited = item.source_reference and (
                previous is not None or any(item.source_reference in text for text in user_messages)
            )
            source_default = item.source_reference if cited else ""
            support_options = _review_field_options("source_support")
            verification_options = _review_field_options("verification")
            judgment_options = _review_field_options("judgment")
            with st.expander(f"Evidence {index + 1}" if proposed else "Add evidence", expanded=proposed):
                claim = st.text_area("Claim or finding", item.claim, key=f"{prefix}_claim")
                if item.source_reference and not cited:
                    st.caption("The proposed reference could not be matched to a user message. Add it if you can confirm its provenance.")
                source = st.text_input("Source reference", source_default, key=f"{prefix}_source")
                support = st.selectbox(
                    "Source support", support_options,
                    index=support_options.index(previous.source_support) if previous else int(bool(source_default)),
                    key=f"{prefix}_support",
                )
                verification = st.selectbox(
                    "Verification", verification_options,
                    index=verification_options.index(previous.verification) if previous else 0,
                    key=f"{prefix}_verification",
                )
                judgment = st.selectbox(
                    "Your assessment", judgment_options,
                    index=judgment_options.index(previous.judgment) if previous else 0,
                    key=f"{prefix}_judgment",
                )
                interpretation = st.text_input(
                    "Your interpretation", previous.interpretation if previous else "",
                    key=f"{prefix}_interpretation",
                )
                notes = st.text_input(
                    "Notes or limitations", previous.notes if previous else item.notes,
                    key=f"{prefix}_notes",
                )
                if st.checkbox("Include evidence", key=f"{prefix}_include"):
                    evidence_fields.append(dict(
                        claim=claim,
                        source_reference=source.strip() or None,
                        source_support=support,
                        verification=verification,
                        judgment=judgment,
                        interpretation=interpretation,
                        notes=notes,
                    ))

        st.markdown("#### Options")
        if not draft.options:
            st.caption("No new options proposed.")
        manual_option = chat.OptionDraft(option="", explicitly_rejected=False, reason="")
        for index, item in enumerate([*draft.options, manual_option]):
            proposed = index < len(draft.options)
            prefix = f"{key}_option_{index}"
            with st.expander(f"Option {index + 1}" if proposed else "Add an option", expanded=proposed):
                description = st.text_input("Option", item.option, key=f"{prefix}_description")
                status = st.selectbox(
                    "Option status", ("Brainstormed", "Rejected by user"),
                    index=int(item.explicitly_rejected), key=f"{prefix}_status"
                )
                rationale = st.text_input("Reason or notes", item.reason, key=f"{prefix}_rationale")
                if st.checkbox("Include option", key=f"{prefix}_include"):
                    option_fields.append(dict(description=description, status=status, rationale=rationale))

        st.markdown("#### Open questions")
        if not draft.open_questions:
            st.caption("No new questions proposed.")
        for index, question in enumerate(draft.open_questions):
            edited = st.text_input("Open question", question, key=f"{key}_question_{index}")
            if st.checkbox("Include question", key=f"{key}_include_question_{index}"):
                question_fields.append(edited)

        with st.expander("Add an open question"):
            added_question = st.text_input("New open question", key=f"{key}_question_new")
            if st.checkbox("Include new question", key=f"{key}_include_question_new"):
                question_fields.append(added_question)

        reality_check = st.text_area(
            "Reality Check",
            draft.reality_check.strip() or pending.brief.reality_check,
            key=f"{key}_reality",
        )
        approved = st.form_submit_button(
            "Approve and switch to Decide" if pending.move_to_decide else "Approve notes"
        )
        discarded = st.form_submit_button("Discard review")
    if discarded:
        workspace.pending_review = None
        workspace.wants_decide = False
        st.rerun()
    if approved:
        try:
            brief = workspace.brief.approve_review(
                for_brief_id=pending.brief.brief_id,
                move_to_decide=pending.move_to_decide,
                evidence=tuple(Evidence(**item) for item in evidence_fields),
                options=tuple(Option(**item) for item in option_fields),
                questions=tuple(OpenQuestion(question=item) for item in question_fields),
                reality_check=reality_check,
            )
        except ValueError as exc:
            _validation_error(exc)
            return
        workspace.brief = brief
        workspace.reviewed_through = len(workspace.turns)
        if pending.move_to_decide:
            workspace.phase_start = len(workspace.turns)
        workspace.pending_review = None
        workspace.wants_decide = False
        st.rerun()


def _record_decision(workspace: Workspace):
    brief = workspace.brief
    with st.expander("Record a human decision"):
        evidence = {item.evidence_id: item.claim for item in brief.evidence}
        rejected = {
            item.option_id: item.description for item in brief.options if item.status == "Rejected by user"
        }
        superseded = {item.supersedes_decision_id for item in brief.decisions}
        current = {
            item.decision_id: item.chosen_option
            for item in brief.decisions if item.decision_id not in superseded
        }
        with st.form(f"decision_{brief.brief_id}", enter_to_submit=False):
            option = st.text_input("Your decision")
            rationale = st.text_area("Why did you choose it?")
            evidence_ids = st.multiselect("Supporting evidence", list(evidence), format_func=evidence.get)
            rejected_ids = st.multiselect("Rejected alternatives", list(rejected), format_func=rejected.get)
            reconsider_if = st.text_input("What would make you reconsider?")
            previous = st.selectbox(
                "Decision to supersede", [None, *current],
                format_func=lambda item: current.get(item, "None"),
            )
            confirmed = st.form_submit_button("Confirm my decision")
        if confirmed:
            try:
                decision = Decision(
                    chosen_option=option,
                    rationale=rationale,
                    evidence_ids=tuple(evidence_ids),
                    rejected_option_ids=tuple(rejected_ids),
                    reconsider_if=reconsider_if,
                    supersedes_decision_id=previous,
                )
                workspace.brief = brief.confirm_decision(decision)
            except ValueError as exc:
                _validation_error(exc)
                return
            st.rerun()


def _edit_project(workspace: Workspace):
    brief = workspace.brief
    project = brief.project
    with st.expander("Edit established project settings"):
        with st.form(f"project_{brief.brief_id}", enter_to_submit=False):
            goal = st.text_area("Project goal", project.goal)
            constraints = st.text_area("Established constraints (one per line)", "\n".join(project.constraints))
            rules = project.collaboration
            expectation = st.text_input("Evidence expectation", rules.evidence_expectation)
            role = st.text_input("AI role", rules.ai_role)
            style = st.text_input("Answer style", rules.answer_style)
            length = st.text_input("Response detail", rules.response_length)
            confirmed = st.form_submit_button("Confirm project changes")
        if confirmed:
            try:
                workspace.brief = brief.update_project(
                    goal,
                    _lines(constraints),
                    CollaborationRules(
                        evidence_expectation=expectation,
                        ai_role=role,
                        answer_style=style,
                        response_length=length,
                    ),
                )
            except ValueError as exc:
                _validation_error(exc)
                return
            st.rerun()


def _prepare_review(workspace: Workspace, api_key: str, model: str, move_to_decide: bool):
    brief = workspace.brief
    turns = workspace.turns[workspace.reviewed_through:]
    if turns:
        try:
            with st.spinner("Preparing notes for review…"):
                draft = chat.draft_review(
                    api_key, model, [chat.project_context(brief), *turns]
                )
        except chat.ChatError as exc:
            st.session_state.toolkit_chat_error = str(exc)
            st.rerun()
    else:
        draft = chat.ReviewDraft(
            evidence=[], options=[], open_questions=[], reality_check=brief.reality_check
        )
    workspace.pending_review = PendingReview(brief, draft, move_to_decide)
    st.rerun()


def render_workspace(workspace: Workspace):
    brief = workspace.brief
    st.subheader(f"Our focus · {brief.focus}")
    st.text(brief.project.goal)
    if workspace.phase_start:
        with st.expander("Research conversation"):
            for turn in workspace.turns[:workspace.phase_start]:
                with st.chat_message(turn.role):
                    st.markdown(turn.content)
    for turn in workspace.turns[workspace.phase_start:]:
        with st.chat_message(turn.role):
            st.markdown(turn.content)

    if brief.focus == "Decide":
        st.markdown("**Reality Check**")
        st.text(brief.reality_check)
        st.caption("Use the approved brief to weigh your options. Confirm your decision when you are ready.")

    markdown = export_markdown(brief)
    with st.expander("View approved session brief"):
        st.markdown(markdown.rsplit("## Machine-readable snapshot", 1)[0])
    st.download_button(
        "Download SESSION_BRIEF.md", markdown, "SESSION_BRIEF.md",
        mime="text/markdown", on_click="ignore"
    )

    if workspace.pending_review:
        _render_review(workspace)
        return

    _record_decision(workspace)
    _edit_project(workspace)

    api_key = _setting("OPENAI_API_KEY")
    if not api_key:
        st.info("Set OPENAI_API_KEY to resume the conversation.")
        return
    error = st.session_state.pop("toolkit_chat_error", None)
    if error:
        st.error(error)
    model = _setting("OPENAI_MODEL") or chat.DEFAULT_MODEL
    if brief.focus == "Research":
        label = "Review handoff to Decide" if workspace.wants_decide else "Prepare handoff to Decide"
        if st.button(label, key="toolkit_handoff"):
            workspace.wants_decide = True
            _prepare_review(workspace, api_key, model, move_to_decide=True)
    if st.button("Review session notes", key="toolkit_review_notes"):
        _prepare_review(workspace, api_key, model, move_to_decide=False)

    with st.container():
        message = st.chat_input(
            "What would you like to explore together?",
            max_chars=12000, disabled=workspace.unsent is not None,
            key="toolkit_chat",
        )
    if workspace.unsent is not None:
        st.text(workspace.unsent)
        if st.button("Discard unsent message", key="toolkit_discard_unsent"):
            workspace.unsent = None
            st.rerun()
        if st.button("Retry message", key="toolkit_retry"):
            message = workspace.unsent
    if not message or not message.strip():
        return

    user_turn = chat.Turn(role="user", content=message)
    try:
        with st.spinner("Thinking through your question…"):
            result = chat.reply_for_brief(
                api_key,
                model,
                brief,
                [*workspace.turns[workspace.phase_start:], user_turn],
            )
    except chat.ChatError as exc:
        workspace.unsent = message
        st.session_state.toolkit_chat_error = str(exc)
        st.rerun()
    workspace.unsent = None
    workspace.turns.extend([user_turn, chat.Turn(role="assistant", content=result.as_markdown())])
    if result.requests_decide and brief.focus == "Research":
        workspace.wants_decide = True
        _prepare_review(workspace, api_key, model, move_to_decide=True)
    st.rerun()
