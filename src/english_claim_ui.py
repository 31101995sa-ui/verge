"""R4.8: human-confirmed English Table IX source-cell input for Streamlit.

Results are supplied only by the existing manifest-validated NASA-EVP router.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pandas as pd
import streamlit as st

from src.claim_text_parser import parse_table_ix_claim
from src.english_claim_flow import verify_confirmed_english_claim
from src.evidence_ledger import make_evidence_entry
from src.i18n import parser_reason, tr


def render_english_claim_input(
    records: pd.DataFrame, release_dir: str | Path, language: str = "en"
) -> None:
    """Preview a candidate and require a second click before verification."""
    with st.expander(tr("english_expander", language), expanded=True):
        st.caption(tr("english_help", language))
        text = st.text_area(
            tr("english_label", language),
            placeholder=tr("english_example", language),
            key="r4_english_claim_text",
            height=100,
        )

        if st.button(tr("parse_button", language), key="r4_english_parse"):
            st.session_state["r4_english_parsed_text"] = text
            st.session_state["r4_english_candidate"] = parse_table_ix_claim(
                text, records
            )

        candidate = st.session_state.get("r4_english_candidate")
        parsed_text = st.session_state.get("r4_english_parsed_text")
        if candidate is None:
            return
        if parsed_text != text:
            st.info(tr("text_changed", language))
            return
        if candidate["parse_status"] != "PARSED":
            st.warning(parser_reason(candidate["reason"], language))
            return

        claim = candidate["claim"]
        st.write(f"**{tr('candidate_only', language)}:**")
        st.json({
            "experiment_id": claim["experiment_id"],
            "claim_class": claim["claim_class"],
            "raw_csv_field": claim["raw_csv_field"],
            "asserted_value": claim["asserted_value"],
            "asserted_unit": claim["asserted_unit"],
            "source_anchor": claim["source_anchor"],
            "data_release_id": claim["data_release_id"],
        })

        if st.button(
            tr("confirm_button", language),
            key="r4_english_confirm",
        ):
            try:
                result = verify_confirmed_english_claim(
                    records,
                    release_dir,
                    original_text=text,
                    candidate=claim,
                )
            except ValueError as exc:
                # The original exception is retained; no physical verdict is inferred.
                st.error(tr("parse_error", language) + ": " + str(exc))
                return

            entries = st.session_state.setdefault("r4_ledger_entries", [])
            run_id = st.session_state.setdefault(
                "r4_ledger_run_id", f"session-{uuid4().hex[:12]}"
            )
            entry = make_evidence_entry(
                claim,
                result,
                sequence=len(entries) + 1,
                run_id=run_id,
                claim_text=text,
            )
            entries.append(entry)
            st.session_state["r4_last_evidence_entry"] = entry
            st.success(tr("confirm_success", language))
