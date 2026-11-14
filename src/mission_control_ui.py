"""Scientific Mission Control presentation only.

Navigation, overview and method notes do not assign scientific verdicts.
All source values and evidence ledgers remain owned by existing modules.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.bassii_d7_loader import BASS_REPORT_URL, load_bassii_d7
from src.flex_d7_loader import RELEASE_ID
from src.i18n import tr

NASA_FLEX_URL = "https://ntrs.nasa.gov/citations/20150023456"
NAV_KEYS = (
    "mc_nav_overview", "mc_nav_explore", "mc_nav_search",
    "mc_nav_verify", "mc_nav_ledger", "mc_nav_methods",
)


def navigation_labels(language: str) -> tuple[str, ...]:
    """Localized tab labels, with stable order in both languages."""
    return tuple(tr(key, language) for key in NAV_KEYS)


def overview_metrics(records: pd.DataFrame) -> dict[str, int]:
    """Counts of D4 records, never a score for scientific confidence."""
    counts = records["qc_dap_d4_record_status"].value_counts()
    return {
        "records": len(records),
        "verified": int(counts.get("VERIFIED", 0)),
        "review": int(counts.get("REVIEW", 0)),
    }


def render_mission_header(language: str) -> None:
    """Compact native Streamlit header matching the research-lab direction."""
    import streamlit as st

    left, right = st.columns([5, 1], vertical_alignment="center")
    with left:
        st.title("◉ VERGE · NASA EDITION")
        st.caption(tr("mc_subtitle", language))
    with right:
        st.caption("FLEX D7 · BASS-II D7")
    st.divider()


def render_overview(records: pd.DataFrame, bass_release_dir: Path, language: str) -> None:
    """Mission-level orientation; BASS-II totals require a valid D7 load."""
    import streamlit as st

    st.subheader(tr("mc_overview_heading", language))
    st.caption(tr("mc_overview_intro", language))

    counts = overview_metrics(records)
    first, second, third = st.columns(3)
    first.metric(tr("source_records", language), counts["records"])
    second.metric(tr("verified_lookup", language), counts["verified"])
    third.metric(tr("needs_review", language), counts["review"])
    st.caption(tr("mc_d4_not_evp", language))

    flex_col, bass_col = st.columns(2)
    with flex_col, st.container(border=True):
        st.markdown("### FLEX · PSI-69")
        st.caption(tr("mc_flex_summary", language))
        st.caption(tr("data_release", language, id=RELEASE_ID))
        st.markdown(f"[{tr('original_report', language)}]({NASA_FLEX_URL})")

    with bass_col, st.container(border=True):
        st.markdown("### BASS-II · PSI-25")
        st.caption(tr("mc_bass_summary", language))
        try:
            cells = load_bassii_d7(bass_release_dir)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            st.error(tr("bass_load_error", language))
            st.code(str(exc))
        else:
            st.metric(tr("mc_method_cells", language), len(cells))
            st.caption(tr("mc_bass_not_tests", language))
        st.markdown(f"[{tr('original_report', language)}]({BASS_REPORT_URL})")

    st.info(tr("mc_workflow", language))
    st.warning(tr("mc_restriction", language))


def render_ledgers(language: str) -> None:
    """Present each independent in-session ledger in its own tab."""
    import streamlit as st

    from src.verification_ui import render_flex_ledger
    from src.bassii_verification_ui import render_bassii_ledger

    st.subheader(tr("mc_ledger_heading", language))
    st.caption(tr("mc_ledger_intro", language))
    flex_tab, bass_tab = st.tabs([
        tr("mc_flex_tab", language), tr("mc_bass_tab", language)
    ])
    with flex_tab:
        render_flex_ledger(language)
    with bass_tab:
        render_bassii_ledger(language)


def render_methods(language: str) -> None:
    """Visible study provenance and strict permitted-use boundaries."""
    import streamlit as st

    st.subheader(tr("mc_methods_heading", language))
    st.info(tr("mc_methods_dap", language))
    st.info(tr("mc_methods_evp", language))

    with st.container(border=True):
        st.markdown("### FLEX · NASA/TP-2015-216046")
        st.write(tr("mc_flex_summary", language))
        st.warning(tr("bounded_warning", language))
        st.markdown(f"[{tr('original_report', language)}]({NASA_FLEX_URL})")

    with st.container(border=True):
        st.markdown("### BASS-II · NASA/TM-20210011385")
        st.write(tr("mc_bass_summary", language))
        st.warning(tr("bass_method_warning", language))
        st.warning(tr("bass_discrepancy", language))
        st.warning(tr("bass_scope", language))
        st.markdown(f"[{tr('original_report', language)}]({BASS_REPORT_URL})")

    st.caption(tr("mc_methods_limit", language))
