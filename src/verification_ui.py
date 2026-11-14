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


def render_verification_panel(records: pd.DataFrame, release_dir: str | Path) -> None:
    """Render structured proof entry, observed verdict, and downloadable ledger."""
    st.divider()
    st.subheader("Evidence Verification — FLEX D7")
    st.caption(
        "Verify structured claims against NASA/TP-2015-216046, Table IX. "
        "The 17-record D7 sample is not a validated prediction dataset. "
        "This form does not interpret free text or search counterexamples."
    )

    with st.form("r4_verification_form"):
        experiment_id = st.selectbox(
            "NASA experiment ID", sorted(records["flex_test_id"].tolist()),
            index=sorted(records["flex_test_id"].tolist()).index("FLEX-002"),
            key="r4_experiment_id",
        )
        claim_class = st.selectbox(
            "Claim class", CLAIM_CLASSES, key="r4_claim_class",
        )

        if claim_class in ("SOURCE_TRANSCRIPTION", "LIMITED_REPORTED_VALUE"):
            fields = (
                ("fuel_raw", *FIELD_RULES)
                if claim_class == "SOURCE_TRANSCRIPTION"
                else tuple(FIELD_RULES)
            )
            raw_field = st.selectbox(
                "Reported Table IX field", fields,
                format_func=lambda field: FIELD_LABELS[field],
                index=fields.index("oxygen_mole_fraction_raw"),
                key="r4_raw_field",
            )
            asserted_value = st.text_input(
                "Asserted value", placeholder="Example: 0.21 or 0.34",
                key="r4_asserted_value",
            ).strip()
            source_unit = (
                "category" if raw_field == "fuel_raw"
                else FIELD_RULES[raw_field][0]
            )
            asserted_unit = st.selectbox(
                "Asserted unit", (source_unit, *[u for u in UNIT_OPTIONS if u != source_unit]),
                key="r4_asserted_unit",
            )
        else:
            raw_field = None
            asserted_value = None
            asserted_unit = None
            st.caption(
                "You selected a policy class. This is a declared classification, "
                "not an automatic interpretation of an English-language claim."
            )

        submitted = st.form_submit_button("Verify structured claim")

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
        st.markdown("#### Latest observed verification")
        claim_description = (
            f"{submitted_claim['experiment_id']} · "
            f"{submitted_claim['claim_class']} · "
            f"{submitted_claim.get('raw_csv_field') or 'scope policy'}"
        )
        st.caption(f"Evaluated claim: {claim_description}")
        if submitted_claim.get("asserted_value") is not None:
            st.write(
                "**Asserted:**", repr(submitted_claim["asserted_value"]),
                submitted_claim["asserted_unit"],
            )

        state = evidence.get("technical_state")
        verdict = evidence.get("verdict")
        explanation = evidence.get("explanation", "")
        if state == "ERROR":
            st.error("Technical ERROR — no scientific verdict. " + explanation)
        elif verdict == "SUPPORTED":
            st.success("SUPPORTED — " + explanation)
        elif verdict == "CONTRADICTED":
            st.error("CONTRADICTED — " + explanation)
        elif verdict == "OUT_OF_SCOPE":
            st.warning("OUT_OF_SCOPE — " + explanation)
        else:
            st.info("INSUFFICIENT_EVIDENCE — " + explanation)

        st.write("**NASA source locator:**", evidence.get("source_anchor") or "Unavailable")
        st.write("**Source raw value:**", repr(evidence.get("source_raw_value")))
        st.write("**Source unit:**", evidence.get("source_unit") or "Not applicable")
        st.write("**D4 QC status:**", evidence.get("source_qc_status") or "Unavailable")
        st.write("**QC flags:**", evidence.get("source_qc_flags") or "Not recorded")
        st.write("**Blocked uses:**", evidence.get("source_blocked_uses") or "Not recorded")
        if evidence.get("field_blocked") is True:
            st.warning("Field-level numerical physical use is blocked by the D7 audit.")
        if evidence.get("source_review_reason"):
            st.write("**Review reason:**", evidence["source_review_reason"])
        st.markdown(f"**Original NASA report:** [NTRS 20150023456]({REPORT_URL})")
        with st.expander("Proof checks and full verifier output"):
            checks = evidence.get("checks", {})
            if checks:
                st.dataframe(
                    pd.DataFrame([
                        {"Check": name, "Result": outcome}
                        for name, outcome in checks.items()
                    ]), hide_index=True, use_container_width=True,
                )
            st.json(evidence)

    entries = st.session_state.get("r4_ledger_entries", [])
    st.markdown("#### Session Evidence Ledger")
    st.caption(
        "This ledger persists only in the current Streamlit session. "
        "Export JSON to retain the observed proofs. No source CSV is changed."
    )
    if entries:
        st.dataframe(
            pd.DataFrame([
                {
                    "Entry": item["sequence"],
                    "Experiment": item["claim"]["experiment_id"],
                    "Class": item["claim"]["claim_class"],
                    "Verdict": item["evaluation"].get("verdict") or "NO_VERDICT",
                    "Technical": item["evaluation"].get("technical_state"),
                    "Source locator": item["evaluation"].get("source_anchor") or "",
                }
                for item in entries
            ]),
            hide_index=True, use_container_width=True,
        )
        st.download_button(
            "Download Evidence Ledger (JSON)",
            data=ledger_as_json(entries),
            file_name="VERGE_FLEX_evidence_ledger.json",
            mime="application/json",
            key="r4_download_ledger",
        )
    else:
        st.caption("No claims evaluated in this session yet.")
