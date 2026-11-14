
# AI-assisted development: ChatGPT (GPT-6).
# Code reviewed and executed by the human project owner.

from pathlib import Path

import streamlit as st

from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.bassii_d7_loader import BASS_RELEASE_ID
from src.bassii_card import render_bassii_card
from src.bassii_verification_ui import render_bassii_verification
from src.mission_control_ui import (
    navigation_labels, render_mission_header, render_overview,
    render_ledgers, render_methods,
)
from src.explorer_filters import filter_flex_records
from src.chart_presentation import make_count_chart
from src.ranking import search_and_rank_flex
from src.verification_ui import render_verification_panel
from src.i18n import display_code, init_language, ranking_reason, source_note, qc_flags_text, tr


RELEASE_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "releases"
    / RELEASE_ID
)

NASA_REPORT_URL = "https://ntrs.nasa.gov/citations/20150023456"
BASS_RELEASE_DIR = Path(__file__).resolve().parent / "data" / "releases" / BASS_RELEASE_ID


def main() -> None:
    st.set_page_config(
        page_title="VERGE — NASA Edition",
        page_icon="🛰️",
        layout="wide",
    )

    # Language and original widget keys remain stable across both locales.
    language = init_language(st.session_state)
    st.sidebar.radio(
        tr("language", language),
        ("en", "ru"),
        key="ui_language",
        format_func=lambda code: "English" if code == "en" else "Русский",
        horizontal=True,
    )
    language = st.session_state["ui_language"]

    # A failed FLEX D7 validation must never lead to a misleading dashboard.
    try:
        records = load_flex_d7_release(RELEASE_DIR)
    except (OSError, ValueError, KeyError) as exc:
        st.error(tr("load_failed", language))
        st.code(str(exc))
        st.stop()
        return

    render_mission_header(language)

    # All tabs render on every rerun, preserving existing Streamlit widget
    # keys and session ledgers when visitors switch pages or language.
    overview_tab, explore_tab, search_tab, verify_tab, ledger_tab, methods_tab = st.tabs(
        navigation_labels(language)
    )

    with overview_tab:
        render_overview(records, BASS_RELEASE_DIR, language)

    with explore_tab:
        st.subheader(tr("explorer", language))
        st.info(tr("bounded_warning", language))
        render_flex_explorer(records, language)
        st.divider()
        render_bassii_card(BASS_RELEASE_DIR, language=language, include_verification=False)

    with search_tab:
        render_evidence_search(records, language)

    with verify_tab:
        flex_tab, bass_tab = st.tabs([
            tr("mc_flex_tab", language), tr("mc_bass_tab", language)
        ])
        with flex_tab:
            render_verification_panel(records, RELEASE_DIR, language=language, show_ledger=False)
        with bass_tab:
            render_bassii_verification(BASS_RELEASE_DIR, language=language, show_ledger=False)

    with ledger_tab:
        render_ledgers(language)

    with methods_tab:
        render_methods(language)


def render_flex_explorer(records, language: str = "en") -> None:
    """Original source-linked FLEX filters, charts and record inspection."""
    # R2.2 — Interactive filters for source-linked experiments.
    st.subheader(tr("filter_heading", language))

    search_col, fuel_col = st.columns([2, 1])

    with search_col:
        test_id_query = st.text_input(
            tr("search_id", language),
            placeholder=tr("id_example", language),
            key="r2_test_id_query",
        )

    with fuel_col:
        selected_fuels = st.multiselect(
            tr("fuel", language),
            options=sorted(records["fuel_raw"].unique().tolist()),
            format_func=lambda value: display_code(value, language),
            key="r2_fuels",
        )

    oxygen_col, outcome_col, qc_col = st.columns(3)

    with oxygen_col:
        selected_oxygen = st.multiselect(
            tr("oxygen_norm", language),
            options=sorted(
                records[
                    "curated_oxygen_mole_fraction"
                ].unique().tolist()
            ),
            help=tr("normalized_help", language),
            key="r2_oxygen",
        )

    with outcome_col:
        selected_outcomes = st.multiselect(
            tr("test_end", language),
            options=sorted(records["test_end_raw"].unique().tolist()),
            format_func=lambda value: display_code(value, language),
            key="r2_outcomes",
        )

    with qc_col:
        selected_qc = st.multiselect(
            tr("d4_status", language),
            options=sorted(
                records[
                    "qc_dap_d4_record_status"
                ].unique().tolist()
            ),
            format_func=lambda value: display_code(value, language),
            key="r2_qc",
        )

    # Reuse the independently tested R2.1 filter.
    filtered_records = filter_flex_records(
        records,
        test_id_query=test_id_query,
        fuels=selected_fuels,
        oxygen_fractions=selected_oxygen,
        outcomes=selected_outcomes,
        qc_statuses=selected_qc,
    )

    st.caption(tr(
        "filter_count", language,
        selected=len(filtered_records), total=len(records),
    ))

    # Source-linked overview.
    display_columns = {
        "flex_test_id": tr("test_id", language),
        "fuel_raw": tr("fuel_raw", language),
        "oxygen_mole_fraction_raw": tr("oxygen_raw", language),
        "ambient_pressure_mmhg_raw": tr("pressure_raw", language),
        "visible_flame_extinction_diameter_mm_raw": (
            tr("extinction_raw", language)
        ),
        "test_end_raw": tr("test_end", language),
        "qc_dap_d4_record_status": tr("d4_status", language),
        "source_anchor": tr("source_locator", language),
    }

    st.dataframe(
        filtered_records[list(display_columns)].rename(
            columns=display_columns
        ),
        hide_index=True,
        use_container_width=True,
    )

    if filtered_records.empty:
        st.warning(tr("empty_filter", language))
        return

    # R2.3 — Descriptive counts for selected D7 records.
    st.subheader(tr("composition", language))

    st.caption(tr(
        "composition_warning", language,
        selected=len(filtered_records), total=len(records), id=RELEASE_ID,
    ))

    # R2 charts: compact labels and zero-based count axes for EN/RU.
    chart_fields = (
        "fuel_raw",
        "test_end_raw",
        "qc_dap_d4_record_status",
    )
    chart_columns = st.columns(3)

    for chart_column, field in zip(chart_columns, chart_fields):
        figure = make_count_chart(filtered_records, field, language)
        with chart_column:
            st.plotly_chart(
                figure,
                use_container_width=True,
                key=f"d7_count_v2_{field}",
            )

    st.divider()
    st.subheader(tr("inspect_record", language))

    # Allow inspection of individual experiments.
    chosen_id = st.selectbox(
        tr("experiment_id", language),
        options=filtered_records["flex_test_id"].tolist(),
        key="r2_selected_id",
    )

    record = filtered_records.set_index(
        "flex_test_id",
        drop=False,
    ).loc[chosen_id]

    status = record["qc_dap_d4_record_status"]

    if status == "REVIEW":
        st.warning(tr("review_warning", language))
    else:
        st.info(tr("verified_warning", language))

    # Show exact provenance and scientific restrictions.
    st.write(
        f"**{tr('source_anchor', language)}:**",
        record["source_anchor"],
    )

    st.write(
        f"**{tr('original_report', language)}:**",
        NASA_REPORT_URL,
    )

    st.write(
        f"**{tr('figure_locator', language)}:**",
        record["qc_appendix_b_anchor"] or tr("not_recorded", language),
    )

    st.write(
        f"**{tr('permitted_uses', language)}:**",
        source_note(record["qc_permitted_uses"], language),
    )

    st.write(
        f"**{tr('blocked_uses', language)}:**",
        source_note(record["qc_blocked_uses"], language),
    )

    st.write(
        f"**{tr('qc_flags', language)}:**",
        qc_flags_text(record["qc_qc_flags"], language) or tr("none_recorded", language),
    )

    st.write(
        f"**{tr('review_reason', language)}:**",
        source_note(record["qc_review_reason"], language)
        or tr("none_recorded", language),
    )

    # Display source strings without numerical conversion.
    st.markdown(f"**{tr('field_limits', language)}**")

    st.write(
        tr("pressure_field", language) + ":",
        repr(record["ambient_pressure_mmhg_raw"]),
        f"| {tr('blocked', language)}:",
        record["curated_pressure_field_blocked"],
    )

    st.write(
        tr("extinction_field", language) + ":",
        repr(
            record["visible_flame_extinction_diameter_mm_raw"]
        ),
        f"| {tr('curated_text', language)}:",
        repr(
            record[
                "curated_visible_flame_extinction_droplet_diameter_mm"
            ]
        ),
        f"| {tr('blocked', language)}:",
        record["curated_extinction_diameter_field_blocked"],
    )

    st.caption(tr("quoted_note", language))

    # Full raw record for source-level inspection.
    with st.expander(
        tr("raw_row", language)
    ):
        raw_columns = [
            "flex_test_id",
            "flex_identifier_raw",
            "test_date_raw",
            "test_time_gmt_raw",
            "fuel_raw",
            "ambient_pressure_mmhg_raw",
            "oxygen_mole_fraction_raw",
            "nitrogen_mole_fraction_raw",
            "carbon_dioxide_mole_fraction_raw",
            "helium_mole_fraction_raw",
            "initial_droplet_diameter_mm_raw",
            "visible_flame_extinction_diameter_mm_raw",
            "burning_rate_mm2_per_s_raw",
            "burn_time_s_raw",
            "test_end_raw",
            "pdf_page_1based",
            "printed_page",
            "table_id",
            "source_anchor",
            "transcription_status",
            "qc_flags",
            "analysis_use",
        ]

        st.json({
            name: record[name]
            for name in raw_columns
        })
        # Original QC narratives stay accessible in English.
        if language == "ru":
            with st.expander(tr("source_note_english", language)):
                st.write(record["qc_review_reason"])
                st.write(record["qc_permitted_uses"])
                st.write(record["qc_blocked_uses"])


def render_evidence_search(records, language: str = "en") -> None:
    """Display source-linked deterministic FLEX metadata search."""

    st.divider()
    st.subheader(tr("evidence_search", language))

    st.caption(tr("search_help", language))

    query = st.text_input(
        tr("search_meta", language),
        placeholder=tr("search_placeholder", language),
        key="r3_evidence_query",
    )

    if not query.strip():
        st.caption(tr("search_intro", language))
        return

    results = search_and_rank_flex(records, query)

    if results.empty:
        st.info(tr("search_empty", language))
        return

    st.caption(tr(
        "search_count", language,
        count=len(results), total=len(records), id=RELEASE_ID,
    ))

    display_columns = {
        "ranking_position": tr("rank", language),
        "flex_test_id": tr("experiment_id", language),
        "fuel_raw": tr("fuel_raw", language),
        "test_end_raw": tr("outcome", language),
        "ranking_relevance_score": tr("lexical_score", language),
        "ranking_reasons": tr("why_matched", language),
        "qc_dap_d4_record_status": tr("d4_qc", language),
        "source_anchor": tr("source_locator", language),
    }

    ranked_display = results[list(display_columns)].copy(deep=True)
    ranked_display["ranking_reasons"] = ranked_display["ranking_reasons"].map(
        lambda text: ranking_reason(text, language)
    )
    for raw_column in ("test_end_raw", "qc_dap_d4_record_status", "fuel_raw"):
        if raw_column in ranked_display.columns:
            ranked_display[raw_column] = ranked_display[raw_column].map(
                lambda value: display_code(value, language)
            )
    st.dataframe(
        ranked_display.rename(columns=display_columns),
        hide_index=True,
        use_container_width=True,
    )

    st.caption(tr("rank_caveat", language))

    chosen_id = st.selectbox(
        tr("inspect_ranked", language),
        options=results["flex_test_id"].tolist(),
        key="r3_selected_evidence_id",
    )

    # Preserve flex_test_id both as index and as a source field.
    chosen = results.set_index(
        "flex_test_id",
        drop=False,
    ).loc[chosen_id]

    if chosen["qc_dap_d4_record_status"] == "REVIEW":
        st.warning(
            tr("d4_review_detail", language) + " "
            + source_note(chosen["qc_review_reason"], language)
        )
    else:
        st.info(tr("d4_verified_detail", language))

    st.write(
        f"**{tr('ranking_explanation', language)}:**",
        ranking_reason(chosen["ranking_reasons"], language),
    )

    st.write(
        f"**{tr('source_locator', language)}:**",
        chosen["source_anchor"],
    )

    st.write(
        f"**{tr('table_reference', language)}:**",
        tr("printed_pdf", language,
           printed=chosen["printed_page"], pdf=chosen["pdf_page_1based"]),
    )

    st.write(
        f"**{tr('original_report', language)}:**",
        NASA_REPORT_URL,
    )

    with st.expander(tr("source_qc_expander", language)):
        st.write(
            f"**{tr('fuel_raw', language)}:**",
            chosen["fuel_raw"],
        )

        st.write(
            f"**{tr('oxygen_source', language)}:**",
            repr(chosen["oxygen_mole_fraction_raw"]),
        )

        st.write(
            f"**{tr('ambient_source', language)}:**",
            repr(chosen["ambient_pressure_mmhg_raw"]),
            f"| {tr('blocked', language)}:",
            chosen["curated_pressure_field_blocked"],
        )

        st.write(
            f"**{tr('visible_source', language)}:**",
            repr(
                chosen[
                    "visible_flame_extinction_diameter_mm_raw"
                ]
            ),
            f"| {tr('blocked', language)}:",
            chosen["curated_extinction_diameter_field_blocked"],
        )

        st.write(
            f"**{tr('permitted_uses', language)}:**",
            source_note(chosen["qc_permitted_uses"], language),
        )

        st.write(
            f"**{tr('blocked_uses', language)}:**",
            source_note(chosen["qc_blocked_uses"], language),
        )

        st.write(
            f"**{tr('qc_flags', language)}:**",
            qc_flags_text(chosen["qc_qc_flags"], language) or tr("none_recorded", language),
        )

        st.write(
            f"**{tr('audited_figure', language)}:**",
            chosen["qc_appendix_b_anchor"]
            or tr("not_in_release", language),
        )
        if language == "ru":
            with st.expander(tr("source_note_english", language)):
                st.write(chosen["qc_review_reason"])
                st.write(chosen["qc_permitted_uses"])
                st.write(chosen["qc_blocked_uses"])


if __name__ == "__main__":
    main()
