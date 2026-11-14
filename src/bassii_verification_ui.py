"""R5.3: bilingual, structured BASS-II NASA-EVP verification in Streamlit.

Not a free-text parser or a safety calculator. Scientific verdicts come only
from src.bassii_evp after independent manifest validation.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pandas as pd

from src.bassii_d7_loader import BASS_RELEASE_ID, BASS_REPORT_URL, load_bassii_d7
from src.bassii_evp import verify_bassii_claim
from src.bassii_ledger import bassii_ledger_as_json, make_bassii_entry
from src.i18n import display_code, tr

_METHOD_KEYS = {
    "EXPERIMENTAL": "bass_method_experiment",
    "COMPUTATIONAL_MODEL": "bass_method_computation",
    "ANALYTICAL_MODEL": "bass_method_theory",
}


def build_bassii_source_claim(
    cells: pd.DataFrame,
    *,
    evidence_cell_id: str,
    asserted_value_raw: str,
    asserted_unit: str,
) -> dict:
    """Resolve one audited method cell; never manufacture an as-run test ID."""
    if not isinstance(asserted_value_raw, str) or not asserted_value_raw.strip():
        raise ValueError("Enter a numeric claim, including reported ± when present")
    if asserted_unit not in ("mm/s", "cm/s"):
        raise ValueError("The UI accepts only mm/s or cm/s")
    required = {"evidence_cell_id", "oxygen_percent_raw", "method_origin", "source_anchor"}
    if not required.issubset(cells.columns):
        raise ValueError("Missing BASS-II source-cell identity fields")
    chosen = cells.loc[cells["evidence_cell_id"] == evidence_cell_id]
    if len(chosen) != 1:
        raise ValueError("Exactly one audited BASS-II evidence cell is required")
    row = chosen.iloc[0]
    return {
        "data_release_id": BASS_RELEASE_ID,
        "claim_class": "SOURCE_TRANSCRIPTION",
        "o2_percent_condition": row["oxygen_percent_raw"],
        "method_origin": row["method_origin"],
        "asserted_value_raw": asserted_value_raw.strip(),
        "asserted_unit": asserted_unit,
        "source_anchor": row["source_anchor"],
    }


def render_bassii_verification(
    release_dir: str | Path, language: str = "en", show_ledger: bool = True
) -> None:
    """Render BASS-II source-cell verification and its separate session ledger."""
    import streamlit as st

    st.markdown("#### " + tr("bass_verify_title", language))
    st.caption(tr("bass_verify_intro", language))
    try:
        cells = load_bassii_d7(release_dir)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        st.error(tr("bass_load_error", language))
        st.code(str(exc))
        return

    by_id = cells.set_index("evidence_cell_id", drop=False)

    def describe_cell(cell_id: str) -> str:
        item = by_id.loc[cell_id]
        method = item["method_origin"]
        return (
            f"{item['oxygen_percent_raw']}% O₂ · "
            f"{tr(_METHOD_KEYS[method], language)} [{method}]"
        )

    with st.form("r5_bassii_verification_form"):
        cell_id = st.selectbox(
            tr("bass_verify_cell", language),
            options=cells["evidence_cell_id"].tolist(),
            format_func=describe_cell,
            key="r5_bassii_verify_cell_id",
        )
        asserted_value = st.text_input(
            tr("asserted_value", language),
            placeholder=tr("bass_verify_example", language),
            key="r5_bassii_verify_value",
        )
        asserted_unit = st.selectbox(
            tr("asserted_unit", language),
            options=("mm/s", "cm/s"),
            key="r5_bassii_verify_unit",
        )
        submit = st.form_submit_button(tr("bass_verify_button", language))

    if submit:
        try:
            claim = build_bassii_source_claim(
                cells,
                evidence_cell_id=cell_id,
                asserted_value_raw=asserted_value,
                asserted_unit=asserted_unit,
            )
        except ValueError as exc:
            st.warning(str(exc))
        else:
            observed = verify_bassii_claim(release_dir, claim)
            entries = st.session_state.setdefault("r5_bassii_ledger_entries", [])
            run_id = st.session_state.setdefault(
                "r5_bassii_ledger_run_id", f"session-{uuid4().hex[:12]}"
            )
            entry = make_bassii_entry(
                claim, observed, sequence=len(entries) + 1, run_id=run_id
            )
            entries.append(entry)
            st.session_state["r5_bassii_last_entry"] = entry

    last = st.session_state.get("r5_bassii_last_entry")
    if last:
        observed = last["evaluation"]
        status = observed.get("technical_state")
        verdict = observed.get("verdict")
        if status == "ERROR":
            st.error(display_code("ERROR", language) + " — " + tr("bass_verify_error", language))
        elif verdict == "SUPPORTED":
            st.success(display_code("SUPPORTED", language) + " — " + tr("bass_verify_supported", language))
        elif verdict == "CONTRADICTED":
            st.error(display_code("CONTRADICTED", language) + " — " + tr("bass_verify_contradicted", language))
        elif verdict == "OUT_OF_SCOPE":
            st.warning(display_code("OUT_OF_SCOPE", language))
        else:
            st.info(display_code("INSUFFICIENT_EVIDENCE", language))

        st.write(f"**{tr('bass_method', language)}:**", observed.get("method_origin") or "—")
        st.write(f"**{tr('bass_o2', language)}:**", str(observed.get("oxygen_percent_condition")) + "%")
        st.write(f"**{tr('source_locator', language)}:**", observed.get("source_anchor") or "—")
        st.write(f"**{tr('source_raw_value', language)}:**", observed.get("source_value_raw") or "—", observed.get("source_unit") or "")
        st.write(f"**{tr('bass_uncertainty', language)}:**",
                 observed.get("experimental_uncertainty_raw") or tr("bass_not_reported", language))
        st.write(f"**{tr('bass_kind', language)}:**", observed.get("value_kind") or "—")
        st.write(f"**{tr('blocked_uses', language)}:**", observed.get("blocked_uses") or "—")
        st.warning(tr("bass_discrepancy", language))
        st.caption(tr("bass_verify_no_asrun", language))
        st.write(f"[{tr('bass_report', language)}]({BASS_REPORT_URL})")
        with st.expander(tr("proof_expander", language)):
            st.write(observed.get("explanation", ""))
            st.json(observed)

    if show_ledger:
        render_bassii_ledger(language)


def render_bassii_ledger(language: str = "en") -> None:
    """Display and export BASS-II evidence separately from FLEX."""
    import streamlit as st
    entries = st.session_state.get("r5_bassii_ledger_entries", [])
    st.markdown("#### " + tr("bass_verify_ledger", language))
    st.caption(tr("bass_verify_ledger_note", language))
    if entries:
        st.dataframe(pd.DataFrame([
            {
                tr("entry", language): item["sequence"],
                tr("bass_method", language): item.get("method_origin"),
                tr("bass_o2", language): str(item.get("oxygen_percent_condition")) + "%",
                tr("verdict", language): display_code(
                    item.get("verdict") or "ERROR", language
                ),
                tr("source_locator", language): (item.get("source_refs") or [""])[0],
            }
            for item in entries
        ]), hide_index=True, use_container_width=True)
        st.download_button(
            tr("bass_verify_download", language),
            data=bassii_ledger_as_json(entries),
            file_name="VERGE_BASSII_evidence_ledger.json",
            mime="application/json",
            key="r5_bassii_ledger_download",
        )
    else:
        st.caption(tr("ledger_empty", language))
