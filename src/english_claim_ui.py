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


def render_english_claim_input(records: pd.DataFrame, release_dir: str | Path) -> None:
    """Preview a candidate and require a second click before verification."""
    with st.expander("English Table IX statement — constrained input", expanded=True):
        st.caption(
            "A restricted single-source-cell grammar, not general free-text AI. "
            "Parsing does not verify claims. Confirm the extracted fields "
            "before the independent NASA-EVP check."
        )
        text = st.text_area(
            "Enter one English Table IX statement",
            placeholder=(
                "NASA Table IX lists an oxygen mole fraction "
                "of 0.21 for FLEX-002."
            ),
            key="r4_english_claim_text",
            height=100,
        )

        if st.button("Parse statement", key="r4_english_parse"):
            st.session_state["r4_english_parsed_text"] = text
            st.session_state["r4_english_candidate"] = parse_table_ix_claim(
                text, records
            )

        candidate = st.session_state.get("r4_english_candidate")
        parsed_text = st.session_state.get("r4_english_parsed_text")
        if candidate is None:
            return
        if parsed_text != text:
            st.info("Text changed. Parse again to inspect the updated statement.")
            return
        if candidate["parse_status"] != "PARSED":
            st.warning(candidate["reason"])
            return

        claim = candidate["claim"]
        st.write("**Candidate only — not yet scientifically verified:**")
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
            "Confirm parsed fields and verify",
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
                st.error(str(exc))
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
            st.success("Confirmed claim evaluated. See verdict and ledger below.")
