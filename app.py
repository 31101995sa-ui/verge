
# AI-assisted development: ChatGPT (GPT-6).
# Code reviewed and executed by the human project owner.

from pathlib import Path

import streamlit as st
import plotly.express as px

from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.explorer_filters import filter_flex_records
from src.explorer_charts import sample_category_counts
from src.ranking import search_and_rank_flex
from src.verification_ui import render_verification_panel


RELEASE_DIR = (
    Path(__file__).resolve().parent
    / "data"
    / "releases"
    / RELEASE_ID
)

NASA_REPORT_URL = "https://ntrs.nasa.gov/citations/20150023456"


def main() -> None:
    st.set_page_config(
        page_title="VERGE-NASA Edition",
        page_icon="🚀",
        layout="wide",
    )

    st.title("VERGE-NASA Edition")
    st.caption("Stellar Anvil | NASA Space Apps Challenge 2026")
    st.subheader("NASA Evidence Explorer — FLEX")

    # Load and validate the bounded D7 scientific release.
    try:
        records = load_flex_d7_release(RELEASE_DIR)
    except (OSError, ValueError, KeyError) as exc:
        st.error("FLEX D7 release validation failed. No data displayed.")
        st.code(str(exc))
        st.stop()
        return

    # Display record counts, not scientific quality scores.
    statuses = records["qc_dap_d4_record_status"].value_counts()

    total_col, verified_col, review_col = st.columns(3)

    total_col.metric("Source-linked records", len(records))
    verified_col.metric(
        "Verified for point lookup",
        int(statuses.get("VERIFIED", 0)),
    )
    review_col.metric(
        "Require review",
        int(statuses.get("REVIEW", 0)),
    )

    st.caption(
        f"Data release: {RELEASE_ID} | "
        "NASA/TP-2015-216046, Table IX"
    )

    st.info(
        "This is a bounded, read-only scientific sample. "
        "QC status does not establish causal relationships, "
        "safety thresholds, or predictions."
    )

    # R3.3 — Independent evidence search across the full D7 release.
    render_evidence_search(records)

    # R4.6 — Independently verified, source-linked structured claims.
    render_verification_panel(records, RELEASE_DIR)

    # R2.2 — Interactive filters for source-linked experiments.
    st.subheader("Filter experiments")

    search_col, fuel_col = st.columns([2, 1])

    with search_col:
        test_id_query = st.text_input(
            "Search by experiment ID",
            placeholder="e.g. FLEX-034",
        )

    with fuel_col:
        selected_fuels = st.multiselect(
            "Fuel",
            options=sorted(records["fuel_raw"].unique().tolist()),
        )

    oxygen_col, outcome_col, qc_col = st.columns(3)

    with oxygen_col:
        selected_oxygen = st.multiselect(
            "O₂ mole fraction (normalized)",
            options=sorted(
                records[
                    "curated_oxygen_mole_fraction"
                ].unique().tolist()
            ),
            help=(
                "Uses audited normalized text for filtering. "
                "Original NASA strings remain unchanged."
            ),
        )

    with outcome_col:
        selected_outcomes = st.multiselect(
            "Reported test end",
            options=sorted(records["test_end_raw"].unique().tolist()),
        )

    with qc_col:
        selected_qc = st.multiselect(
            "D4 QC status",
            options=sorted(
                records[
                    "qc_dap_d4_record_status"
                ].unique().tolist()
            ),
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

    st.caption(
        f"Showing {len(filtered_records)} of {len(records)} "
        "audited FLEX records. "
        "Empty filter selections mean 'all'."
    )

    # Source-linked overview.
    display_columns = {
        "flex_test_id": "Test ID",
        "fuel_raw": "Fuel (raw)",
        "oxygen_mole_fraction_raw": "O₂ mole fraction (raw)",
        "ambient_pressure_mmhg_raw": "Pressure (raw, mmHg)",
        "visible_flame_extinction_diameter_mm_raw": (
            "Droplet diameter at visible flame extinction (raw, mm)"
        ),
        "test_end_raw": "Reported test end",
        "qc_dap_d4_record_status": "D4 QC status",
        "source_anchor": "NASA source locator",
    }

    st.dataframe(
        filtered_records[list(display_columns)].rename(
            columns=display_columns
        ),
        hide_index=True,
        use_container_width=True,
    )

    if filtered_records.empty:
        st.warning(
            "No experiments match the selected filters. "
            "Try changing or clearing your selections."
        )
        st.stop()

    # R2.3 — Descriptive counts for selected D7 records.
    st.subheader("Audited sample composition")

    st.caption(
        f"Showing categorical counts for {len(filtered_records)} "
        f"selected records out of {len(records)} in the bounded "
        f"FLEX D7 sample ({RELEASE_ID}). "
        "These counts are not representative of all FLEX tests. "
        "No causal comparison or physical prediction is implied."
    )

    chart_definitions = (
        ("fuel_raw", "Fuel"),
        ("test_end_raw", "Reported test end"),
        ("qc_dap_d4_record_status", "D4 QC status"),
    )

    chart_columns = st.columns(3)

    for chart_column, (field, chart_title) in zip(
        chart_columns,
        chart_definitions,
    ):
        counts = sample_category_counts(
            filtered_records,
            field,
        )

        figure = px.bar(
            counts,
            x="category",
            y="sample_records",
            text="sample_records",
            title=chart_title,
            labels={
                "category": chart_title,
                "sample_records": "Audited records",
            },
        )

        figure.update_yaxes(
            rangemode="tozero",
        )

        figure.update_layout(
            showlegend=False,
            margin=dict(
                l=10,
                r=10,
                t=45,
                b=10,
            ),
        )

        with chart_column:
            st.plotly_chart(
                figure,
                use_container_width=True,
                key=f"d7_count_{field}",
            )

    st.divider()
    st.subheader("Inspect a source record")

    # Allow inspection of individual experiments.
    chosen_id = st.selectbox(
        "Experiment ID",
        options=filtered_records["flex_test_id"].tolist(),
    )

    record = filtered_records.set_index(
        "flex_test_id",
        drop=False,
    ).loc[chosen_id]

    status = record["qc_dap_d4_record_status"]

    if status == "REVIEW":
        st.warning(
            "REVIEW — unresolved source or interpretation "
            "limitations apply."
        )
    else:
        st.info(
            "VERIFIED for limited source-point lookup "
            "and display only."
        )

    # Show exact provenance and scientific restrictions.
    st.write(
        "**Source locator:**",
        record["source_anchor"],
    )

    st.write(
        "**NASA original report:**",
        NASA_REPORT_URL,
    )

    st.write(
        "**Appendix B locator:**",
        record["qc_appendix_b_anchor"] or "Not recorded",
    )

    st.write(
        "**Permitted uses:**",
        record["qc_permitted_uses"],
    )

    st.write(
        "**Blocked uses:**",
        record["qc_blocked_uses"],
    )

    st.write(
        "**QC flags:**",
        record["qc_qc_flags"] or "None recorded",
    )

    st.write(
        "**Review reason:**",
        record["qc_review_reason"] or "None recorded",
    )

    # Display source strings without numerical conversion.
    st.markdown(
        "**Field-level restrictions and raw value preservation**"
    )

    st.write(
        "Pressure (raw mmHg):",
        repr(record["ambient_pressure_mmhg_raw"]),
        "| Blocked:",
        record["curated_pressure_field_blocked"],
    )

    st.write(
        "Extinction droplet diameter (raw mm):",
        repr(
            record["visible_flame_extinction_diameter_mm_raw"]
        ),
        "| Curated text:",
        repr(
            record[
                "curated_visible_flame_extinction_droplet_diameter_mm"
            ]
        ),
        "| Blocked:",
        record["curated_extinction_diameter_field_blocked"],
    )

    st.caption(
        "Quoted values distinguish literal '0', "
        "missing '–', and empty ''."
    )

    # Full raw record for source-level inspection.
    with st.expander(
        "Original NASA Table IX row — unchanged strings"
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


def render_evidence_search(records) -> None:
    """Display source-linked deterministic FLEX metadata search."""

    st.divider()
    st.subheader("Evidence Search — FLEX D7")

    st.caption(
        "Literal keyword search across 17 audited records. "
        "All query terms must match within one record. "
        "Ranking is lexical relevance, not scientific confidence "
        "or verification."
    )

    query = st.text_input(
        "Search experiment and QC metadata",
        placeholder="e.g. FLEX-034 or Heptane VERIFIED",
        key="r3_evidence_query",
    )

    if not query.strip():
        st.caption(
            "Enter one or more search terms to inspect "
            "NASA-linked records."
        )
        return

    results = search_and_rank_flex(records, query)

    if results.empty:
        st.info(
            "No matching records in the bounded FLEX D7 release."
        )
        return

    st.caption(
        f"{len(results)} matching record(s) from the "
        f"{len(records)}-record {RELEASE_ID} release."
    )

    display_columns = {
        "ranking_position": "Rank",
        "flex_test_id": "Experiment ID",
        "fuel_raw": "Fuel (raw)",
        "test_end_raw": "Reported outcome",
        "ranking_relevance_score": "Lexical score",
        "ranking_reasons": "Why matched",
        "qc_dap_d4_record_status": "D4 QC",
        "source_anchor": "NASA source locator",
    }

    st.dataframe(
        results[list(display_columns)].rename(
            columns=display_columns
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.caption(
        "Lexical scores are relative search weights, "
        "not percentages, reliability estimates, "
        "fire-risk scores or NASA-EVP verdicts."
    )

    chosen_id = st.selectbox(
        "Inspect ranked result",
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
            "D4 REVIEW — "
            + (
                chosen["qc_review_reason"]
                or "Review restrictions apply."
            )
        )
    else:
        st.info(
            "D4 VERIFIED for limited point lookup only."
        )

    st.write(
        "**Ranking explanation:**",
        chosen["ranking_reasons"],
    )

    st.write(
        "**NASA source locator:**",
        chosen["source_anchor"],
    )

    st.write(
        "**Table IX reference:**",
        f"printed p.{chosen['printed_page']}; "
        f"PDF p.{chosen['pdf_page_1based']}",
    )

    st.write(
        "**Original NASA report:**",
        NASA_REPORT_URL,
    )

    with st.expander("Source values and QC restrictions"):
        st.write(
            "**Fuel (raw):**",
            chosen["fuel_raw"],
        )

        st.write(
            "**Oxygen mole fraction (raw; dimensionless):**",
            repr(chosen["oxygen_mole_fraction_raw"]),
        )

        st.write(
            "**Ambient pressure (raw; mmHg):**",
            repr(chosen["ambient_pressure_mmhg_raw"]),
            "| Blocked:",
            chosen["curated_pressure_field_blocked"],
        )

        st.write(
            "**Droplet diameter at visible flame extinction "
            "(raw; mm):**",
            repr(
                chosen[
                    "visible_flame_extinction_diameter_mm_raw"
                ]
            ),
            "| Blocked:",
            chosen["curated_extinction_diameter_field_blocked"],
        )

        st.write(
            "**Permitted uses:**",
            chosen["qc_permitted_uses"],
        )

        st.write(
            "**Blocked uses:**",
            chosen["qc_blocked_uses"],
        )

        st.write(
            "**QC flags:**",
            chosen["qc_qc_flags"] or "None recorded",
        )

        st.write(
            "**Audited figure locator:**",
            chosen["qc_appendix_b_anchor"]
            or "Not recorded in this release",
        )


if __name__ == "__main__":
    main()
