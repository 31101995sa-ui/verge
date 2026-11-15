"""Optional LOCAL-ONLY Gemini UI; not a public API gateway or scientific verifier."""
from __future__ import annotations

import os
from pathlib import Path

from src.gemini_candidate import CandidateRejected, GeminiCallError, generate_candidate
from src.gemini_evidence import build_bassii_snippets, build_flex_snippets


def local_gemini_enabled(flag: str | None, bind_address: str | None) -> bool:
    """Fail closed unless manually enabled on the local loopback interface."""
    return flag == "1" and bind_address in {"127.0.0.1", "localhost"}


def render_gemini_local_panel(
    flex_release_dir: str | Path,
    bassii_release_dir: str | Path,
    language: str = "en",
) -> None:
    """Render local candidate-generation form without changing EVP or D7 files."""
    import streamlit as st

    if not local_gemini_enabled(
        os.getenv("VERGE_ENABLE_GEMINI_LOCAL"), st.get_option("server.address")
    ):
        return

    ru = language == "ru"
    st.divider()
    st.subheader("AI Evidence Interpretation · Gemini (LOCAL DEMO)")
    st.warning(
        "Черновик Gemini, НЕ научный вердикт. Вызов API разрешён только локально."
        if ru else
        "Gemini draft, NOT a scientific verdict. API use is enabled only locally."
    )

    study = st.radio(
        "Исследование" if ru else "Study",
        ("FLEX", "BASS-II"),
        horizontal=True,
        key="r6_local_study",
    )
    try:
        choices = (
            build_flex_snippets(flex_release_dir)
            if study == "FLEX"
            else build_bassii_snippets(bassii_release_dir)
        )
    except (OSError, ValueError, KeyError) as exc:
        # Do not send any payload to Gemini when a D7 validation fails.
        st.error("D7 integrity/selection failed; Gemini is disabled for this study.")
        st.code(type(exc).__name__)
        return

    by_id = {item.evidence_id: item for item in choices}
    defaults = (
        [item.evidence_id for item in choices[:2]]
        if study == "FLEX"
        else [item.evidence_id for item in choices if "|EXPERIMENTAL" in item.evidence_id]
    )
    if study == "FLEX":
        st.caption(
            "Только 10 строк D4 VERIFIED; 7 REVIEW исключены из LLM-ввода."
            if ru else
            "Only 10 D4 VERIFIED rows; 7 REVIEW rows excluded from LLM intake."
        )
    else:
        st.caption(
            "6 ячеек трёх методов, не 6 независимых опытов."
            if ru else
            "6 method-specific cells, NOT 6 independent experiments."
        )

    selected_ids = st.multiselect(
        "Доказательства (1–4)" if ru else "Evidence cells (1–4)",
        options=list(by_id),
        default=defaults,
        max_selections=4,
        key="r6_local_flex_ids" if study == "FLEX" else "r6_local_bassii_ids",
    )
    selected = [by_id[ref] for ref in selected_ids]
    if selected:
        with st.expander("Проверенные входные данные D7" if ru else "Validated D7 inputs"):
            for item in selected:
                st.markdown(f"**`{item.evidence_id}`**")
                st.code(item.source_locator)
                st.write(item.source_text)
                st.caption(item.restrictions)

    default_question = (
        "Explain what these FLEX records report and what cannot be inferred from them. "
        "Do not claim causation or general safety thresholds."
        if study == "FLEX" else
        "Explain the reported BASS-II method cells and limits of their comparison. "
        "Do not claim causation or safety thresholds."
    )
    with st.form("r6_local_gemini_form"):
        question = st.text_area(
            "Вопрос (русский или английский)" if ru else "Question (Russian or English)",
            value=default_question,
            max_chars=500,
            key="r6_local_question_flex" if study == "FLEX" else "r6_local_question_bassii",
        )
        key = st.text_input(
            "Gemini API key (локально, скрыто)" if ru else "Gemini API key (local, hidden)",
            type="password",
            help="Never enter a key on a hosted/public version of VERGE.",
        )
        submit = st.form_submit_button(
            "Сгенерировать черновик" if ru else "Generate candidate draft"
        )

    if submit:
        if not selected:
            st.error("Select at least one evidence cell.")
        elif not key.strip():
            st.error("Enter your Gemini API key locally (never in GitHub).")
        else:
            try:
                result = generate_candidate(question, selected, api_key=key.strip())
            except (CandidateRejected, GeminiCallError) as exc:
                # The provider exception is already sanitized by the adapter.
                st.warning(f"No accepted draft: {exc}")
                st.session_state.pop("r6_local_last_candidate", None)
            else:
                st.session_state["r6_local_last_candidate"] = (
                    study, tuple(selected_ids), result
                )

    last = st.session_state.get("r6_local_last_candidate")
    if last and last[0] == study and last[1] == tuple(selected_ids):
        result = last[2]
        st.info("CANDIDATE_NOT_VERIFIED · CITATION_IDS_AND_FORMAT_ONLY")
        st.write(result["interpretation"])
        st.markdown("**Limitations**")
        for limit in result["limitations"]:
            st.write(f"- {limit}")
        st.markdown("**NASA D7 evidence locators**")
        for ref in result["cited_evidence_ids"]:
            st.code(f"{ref}  →  {result['source_locators'][ref]}")
        st.caption(
            "Text and citations were format/ID checked only. Scientific meaning "
            "is not independently verified; original measurements are in the D7 inputs."
        )
