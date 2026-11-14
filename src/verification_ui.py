"""R4.6: Streamlit verification UI driven exclusively by NASA-EVP router.

A visitor submits a structured assertion; the verifier independently checks
manifest-validated D7 files. R3 ranking and D4 status do not assign verdicts.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pandas as pd
import streamlit as st

from src.claim_router import REPORT_URL, verify_claim_from_release
from src.evidence_ledger import ledger_as_json, make_evidence_entry
from src.i18n import display_code, field_label, source_note, qc_flags_text, tr, verifier_summary
from src.english_claim_ui import render_english_claim_input
from src.field_evidence import FIELD_RULES
from src.flex_d7_loader import RELEASE_ID
from src.scope_gate import SCOPE_RULES

FIELD_LABELS = {
    "fuel_raw": "Fuel (category)",
    "oxygen_mole_fraction_raw": "Oxygen mole fraction",
    "initial_droplet_diameter_mm_raw": "Initial droplet diameter",
    "visible_flame_extinction_diameter_mm_raw": "Droplet diameter at visible-flame extinction",
    "ambient_pressure_mmhg_raw": "Ambient pressure",
    "burning_rate_mm2_per_s_raw": "Average burning-rate constant",
    "burn_time_s_raw": "Burn time",
}
UNIT_OPTIONS = (
    "dimensionless mole fraction", "%", "percent", "mm", "cm",
    "mmHg", "s", "mm²/s", "category",
)
CLAIM_CLASSES = (
    "SOURCE_TRANSCRIPTION",
    "LIMITED_REPORTED_VALUE",
    *SCOPE_RULES,
)


def render_verification_panel(
    records: pd.DataFrame, release_dir: str | Path, language: str = "en",
    show_ledger: bool = True,
) -> None:
    """Render structured proof entry, observed verdict, and downloadable ledger."""
    st.divider()
    st.subheader(tr("verification", language))
    st.caption(tr("verification_intro", language))

    render_english_claim_input(records, release_dir, language=language)

    with st.form("r4_verification_form"):
        experiment_id = st.selectbox(
            tr("nasa_id", language), sorted(records["flex_test_id"].tolist()),
            index=sorted(records["flex_test_id"].tolist()).index("FLEX-002"),
            key="r4_experiment_id",
        )
        claim_class = st.selectbox(
            tr("claim_class", language), CLAIM_CLASSES,
            format_func=lambda value: display_code(value, language),
            key="r4_claim_class",
        )

        if claim_class in ("SOURCE_TRANSCRIPTION", "LIMITED_REPORTED_VALUE"):
            fields = (
                ("fuel_raw", *FIELD_RULES)
                if claim_class == "SOURCE_TRANSCRIPTION"
                else tuple(FIELD_RULES)
            )
            raw_field = st.selectbox(
                tr("reported_field", language), fields,
                format_func=lambda field: field_label(field, language, FIELD_LABELS[field]),
                index=fields.index("oxygen_mole_fraction_raw"),
                key="r4_raw_field",
            )
            asserted_value = st.text_input(
                tr("asserted_value", language),
                placeholder=tr("value_placeholder", language),
                key="r4_asserted_value",
            ).strip()
            source_unit = (
                "category" if raw_field == "fuel_raw"
                else FIELD_RULES[raw_field][0]
            )
            asserted_unit = st.selectbox(
                tr("asserted_unit", language),
                (source_unit, *[u for u in UNIT_OPTIONS if u != source_unit]),
                key="r4_asserted_unit",
            )
        else:
            raw_field = None
            asserted_value = None
            asserted_unit = None
            st.caption(tr("scope_notice", language))

        submitted = st.form_submit_button(tr("verify_button", language))

    if submitted:
        # The source locator is taken from the audited row selected in the UI;
        # the independent verifier checks it against a fresh manifest-checked load.
        row = records.set_index("flex_test_id", drop=False).loc[experiment_id]
        claim = {
            "data_release_id": RELEASE_ID,
            "claim_class": claim_class,
            "experiment_id": experiment_id,
            "raw_csv_field": raw_field,
            "asserted_value": asserted_value,
            "asserted_unit": asserted_unit,
            "source_anchor": row["source_anchor"],
        }
        result = verify_claim_from_release(release_dir, claim)
        if "r4_ledger_entries" not in st.session_state:
            st.session_state["r4_ledger_entries"] = []
        if "r4_ledger_run_id" not in st.session_state:
            st.session_state["r4_ledger_run_id"] = f"session-{uuid4().hex[:12]}"
        entry = make_evidence_entry(
            claim, result,
            sequence=len(st.session_state["r4_ledger_entries"]) + 1,
            run_id=st.session_state["r4_ledger_run_id"],
        )
        st.session_state["r4_ledger_entries"].append(entry)
        st.session_state["r4_last_evidence_entry"] = entry

    last = st.session_state.get("r4_last_evidence_entry")
    if last:
        evidence = last["evaluation"]
        submitted_claim = last["claim"]
        st.markdown("#### " + tr("latest_verification", language))
        claim_description = (
            f"{submitted_claim['experiment_id']} · "
            f"{submitted_claim['claim_class']} · "
            f"{submitted_claim.get('raw_csv_field') or tr('scope_policy', language)}"
        )
        st.caption(tr("evaluated_claim", language, desc=claim_description))
        if last.get("claim_text") is not None:
            st.write(f"**{tr('confirmed_english', language)}:**", last["claim_text"])
        if submitted_claim.get("asserted_value") is not None:
            st.write(
                f"**{tr('asserted', language)}:**", repr(submitted_claim["asserted_value"]),
                submitted_claim["asserted_unit"],
            )

        state = evidence.get("technical_state")
        verdict = evidence.get("verdict")
        explanation = evidence.get("explanation", "")
        presented = verifier_summary(evidence, language)
        if state == "ERROR":
            st.error(display_code("ERROR", language) + " — " + presented)
        elif verdict == "SUPPORTED":
            st.success(display_code("SUPPORTED", language) + " — " + presented)
        elif verdict == "CONTRADICTED":
            st.error(display_code("CONTRADICTED", language) + " — " + presented)
        elif verdict == "OUT_OF_SCOPE":
            st.warning(display_code("OUT_OF_SCOPE", language) + " — " + presented)
        else:
            st.info(display_code("INSUFFICIENT_EVIDENCE", language) + " — " + presented)
        if language == "ru":
            with st.expander(tr("verifier_original", language)):
                st.write(explanation)

        st.write(f"**{tr('source_locator', language)}:**", evidence.get("source_anchor") or tr("not_recorded", language))
        st.write(f"**{tr('source_raw_value', language)}:**", repr(evidence.get("source_raw_value")))
        st.write(f"**{tr('source_unit', language)}:**", evidence.get("source_unit") or tr("not_applicable", language))
        st.write(f"**{tr('source_qc_status', language)}:**", display_code(evidence.get("source_qc_status"), language)
            if evidence.get("source_qc_status") else tr("not_recorded", language))
        st.write(f"**{tr('qc_flags', language)}:**", qc_flags_text(evidence.get("source_qc_flags") or "", language) or tr("not_recorded", language))
        st.write(f"**{tr('blocked_uses', language)}:**", source_note(evidence.get("source_blocked_uses") or "", language)
            or tr("not_recorded", language))
        if evidence.get("field_blocked") is True:
            st.warning(tr("physical_block", language))
        if evidence.get("source_review_reason"):
            st.write(
                f"**{tr('review_reason', language)}:**",
                source_note(evidence["source_review_reason"], language),
            )
        st.markdown(f"**{tr('original_report', language)}:** [NTRS 20150023456]({REPORT_URL})")
        with st.expander(tr("proof_expander", language)):
            checks = evidence.get("checks", {})
            if checks:
                st.dataframe(
                    pd.DataFrame([
                        {tr("check", language): name, tr("result", language): outcome}
                        for name, outcome in checks.items()
                    ]), hide_index=True, use_container_width=True,
                )
            st.json(evidence)

    if show_ledger:
        render_flex_ledger(language)


def render_flex_ledger(language: str = "en") -> None:
    """Display and export the existing FLEX session-only ledger."""
    entries = st.session_state.get("r4_ledger_entries", [])
    st.markdown("#### " + tr("ledger", language))
    st.caption(tr("ledger_caveat", language))
    if entries:
        st.dataframe(
            pd.DataFrame([
                {
                    tr("entry", language): item["sequence"],
                    tr("experiment", language): item["claim"]["experiment_id"],
                    tr("class", language): display_code(item["claim"]["claim_class"], language),
                    tr("verdict", language): display_code(item["evaluation"].get("verdict") or "NO_VERDICT", language),
                    tr("technical", language): display_code(item["evaluation"].get("technical_state"), language),
                    tr("source_locator", language): item["evaluation"].get("source_anchor") or "",
                }
                for item in entries
            ]),
            hide_index=True, use_container_width=True,
        )
        st.download_button(
            tr("download_ledger", language),
            data=ledger_as_json(entries),
            file_name="VERGE_FLEX_evidence_ledger.json",
            mime="application/json",
            key="r4_download_ledger",
        )
    else:
        st.caption(tr("ledger_empty", language))
