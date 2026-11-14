"""R5: bilingual, read-only BASS-II Table 2.1 Evidence Card.

No BASS-II NASA-EVP verdicts are issued by this UI.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.bassii_d7_loader import BASS_RELEASE_ID, BASS_REPORT_URL, load_bassii_d7
from src.i18n import tr

_METHOD_LABEL_KEYS = {
    "EXPERIMENTAL": "bass_method_experiment",
    "COMPUTATIONAL_MODEL": "bass_method_computation",
    "ANALYTICAL_MODEL": "bass_method_theory",
}


def bassii_display_table(records: pd.DataFrame, language: str) -> pd.DataFrame:
    """Create labels for UI without changing original evidence values or units."""
    displayed = []
    for _, item in records.iterrows():
        method = item["method_origin"]
        label = f"{method} — {tr(_METHOD_LABEL_KEYS[method], language)}" if language == "ru" else tr(_METHOD_LABEL_KEYS[method], language)
        uncertainty = (
            f"{item['experimental_uncertainty_raw']} mm/s"
            if method == "EXPERIMENTAL"
            else tr("bass_not_reported", language)
        )
        displayed.append({
            tr("bass_o2", language): item["oxygen_percent_raw"] + "%",
            tr("bass_method", language): label,
            tr("bass_kind", language): item["value_kind"],
            tr("bass_velocity", language): item["critical_velocity_raw"] + " mm/s",
            tr("bass_uncertainty", language): uncertainty,
        })
    return pd.DataFrame(displayed)


def render_bassii_card(
    release_dir: str | Path, language: str = "en", include_verification: bool = True
) -> None:
    """Present the six source-linked results and their QC limitations."""
    # Kept inside rendering function so pure presentation tests need no Streamlit.
    import streamlit as st

    st.divider()
    st.subheader(tr("bass_title", language))
    try:
        records = load_bassii_d7(release_dir)
    except (OSError, ValueError, KeyError) as exc:
        st.error(tr("bass_load_error", language))
        st.code(str(exc))
        return

    st.caption(tr("bass_intro", language, release=BASS_RELEASE_ID))
    st.write(f"[{tr('bass_report', language)}]({BASS_REPORT_URL})")
    st.info(tr("bass_method_warning", language))

    choice = st.selectbox(
        tr("bass_condition", language),
        options=("all", "21", "16"),
        key="r5_bassii_o2",
        format_func=lambda value: (
            tr("bass_all", language) if value == "all" else value + "% O₂"
        ),
    )
    selected = (
        records if choice == "all"
        else records.loc[records["oxygen_percent_raw"] == choice]
    )
    st.dataframe(
        bassii_display_table(selected, language),
        hide_index=True,
        use_container_width=True,
    )
    st.warning(tr("bass_discrepancy", language))
    st.warning(tr("bass_scope", language))
    st.caption(tr("bass_no_evp", language))

    with st.expander(tr("bass_provenance", language)):
        st.dataframe(
            selected[[
                "evidence_cell_id", "method_origin", "original_test_id",
                "source_anchor", "qc_quality_flags", "qc_blocked_uses",
                "qc_comparison_warning", "qc_original_test_linkage",
            ]],
            hide_index=True,
            use_container_width=True,
        )
        st.caption(tr("bass_original_id_note", language))

    # R5.3: method-specific verification is separate from FLEX.
    if include_verification:
        from src.bassii_verification_ui import render_bassii_verification
        render_bassii_verification(release_dir, language=language)
