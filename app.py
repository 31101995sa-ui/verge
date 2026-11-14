
# AI-assisted development: ChatGPT (GPT-6).
# Code reviewed and executed by the human project owner.

from pathlib import Path

import streamlit as st

from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release


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
        records[list(display_columns)].rename(
            columns=display_columns
        ),
        hide_index=True,
        use_container_width=True,
    )

    st.divider()
    st.subheader("Inspect a source record")

    # Allow inspection of individual experiments.
    chosen_id = st.selectbox(
        "Experiment ID",
        options=records["flex_test_id"].tolist(),
    )

    record = records.set_index("flex_test_id", drop=False).loc[chosen_id]
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


if __name__ == "__main__":
    main()
