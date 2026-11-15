"""Build bounded Gemini inputs exclusively from manifest-validated D7 releases.

D4 VERIFIED means transcription/QC review, not physical validation or EVP SUPPORT.
FLEX REVIEW rows remain inspectable elsewhere but are excluded from LLM intake.
"""
from __future__ import annotations

from pathlib import Path

from src.bassii_d7_loader import load_bassii_d7
from src.flex_d7_loader import load_flex_d7_release
from src.gemini_candidate import EvidenceSnippet


def _raw(value: object) -> str:
    """Preserve original source strings; make an actual blank visibly nonnumeric."""
    text = str(value)
    return "[BLANK_IN_SOURCE]" if text == "" else text


def build_flex_snippets(release_dir: str | Path) -> list[EvidenceSnippet]:
    """Use only the ten D4-VERIFIED FLEX Table IX records (no REVIEW rows)."""
    records = load_flex_d7_release(release_dir)
    verified = records.loc[records["qc_dap_d4_record_status"] == "VERIFIED"]
    if len(verified) != 10:
        raise ValueError("Unexpected FLEX D4 VERIFIED record count")

    snippets: list[EvidenceSnippet] = []
    for _, row in verified.iterrows():
        # Do not present a blocked source field to Gemini as analysis-ready.
        if row["curated_pressure_field_blocked"] == "TRUE":
            raise ValueError("FLEX pressure field blocked in VERIFIED LLM selection")
        if row["curated_extinction_diameter_field_blocked"] == "TRUE":
            raise ValueError("FLEX extinction diameter blocked in VERIFIED LLM selection")
        source_text = (
            "NASA/TP-2015-216046 Table IX, selected source row; "
            f"test ID: {_raw(row['flex_test_id'])}; "
            f"fuel: {_raw(row['fuel_raw'])}; "
            f"ambient pressure: {_raw(row['ambient_pressure_mmhg_raw'])} mmHg; "
            f"oxygen mole fraction: {_raw(row['oxygen_mole_fraction_raw'])}; "
            f"initial droplet diameter: {_raw(row['initial_droplet_diameter_mm_raw'])} mm; "
            "droplet diameter at visible flame extinction: "
            f"{_raw(row['visible_flame_extinction_diameter_mm_raw'])} mm; "
            f"burning rate: {_raw(row['burning_rate_mm2_per_s_raw'])} mm2/s; "
            f"burn time: {_raw(row['burn_time_s_raw'])} s; "
            f"reported test end: {_raw(row['test_end_raw'])}. "
            "Do not confuse extinction droplet diameter with flame diameter."
        )
        restrictions = (
            "D4 transcription/QC status: VERIFIED; not a scientific verdict. "
            f"QC flags: {_raw(row['qc_qc_flags'])}. "
            f"Blocked uses: {_raw(row['qc_blocked_uses'])}. "
            "No cross-test causal inference, physical safety threshold, "
            "Moon/Mars extrapolation or unsupported comparison."
        )
        snippet = EvidenceSnippet(
            study="FLEX",
            evidence_id=str(row["flex_test_id"]),
            source_locator=str(row["source_anchor"]),
            source_text=source_text,
            restrictions=restrictions,
        )
        if len(source_text) > 1200 or len(restrictions) > 700:
            raise ValueError("FLEX evidence too large for bounded Gemini contract")
        snippets.append(snippet)
    return snippets


def build_bassii_snippets(release_dir: str | Path) -> list[EvidenceSnippet]:
    """Keep BASS-II method origins distinct; values are report cells, not runs."""
    records = load_bassii_d7(release_dir)
    if len(records) != 6:
        raise ValueError("Unexpected BASS-II evidence-cell count")
    snippets: list[EvidenceSnippet] = []
    for _, cell in records.iterrows():
        source_text = (
            "NASA/TM-20210011385 Table 2.1, reported summary cell; "
            f"nominal oxygen: {_raw(cell['oxygen_percent_raw'])} percent; "
            f"method: {_raw(cell['method_origin'])}; "
            f"value kind: {_raw(cell['value_kind'])}; "
            "reported critical opposed-flow velocity: "
            f"{_raw(cell['critical_velocity_raw'])} "
            f"{_raw(cell['critical_velocity_raw_unit'])}; "
            f"experimental uncertainty as printed: {_raw(cell['experimental_uncertainty_raw'])}; "
            f"uncertainty status: {_raw(cell['uncertainty_status'])}; "
            f"fuel: {_raw(cell['material_raw'])}; "
            f"pressure: {_raw(cell['pressure_raw'])}; "
            f"gravity: {_raw(cell['gravity_regime'])}. "
            "The model and experiment methods are not independent experiments."
        )
        restrictions = (
            f"Scientific fitness: {_raw(cell['scientific_fitness_status'])}. "
            f"QC blocked uses: {_raw(cell['qc_blocked_uses'])}. "
            f"Comparison warning: {_raw(cell['qc_comparison_warning'])}. "
            "No unique as-run test ID mapping; no universal safety rule."
        )
        snippet = EvidenceSnippet(
            study="BASS-II",
            evidence_id=str(cell["evidence_cell_id"]),
            source_locator=str(cell["source_anchor"]),
            source_text=source_text,
            restrictions=restrictions,
        )
        if len(source_text) > 1200 or len(restrictions) > 700:
            raise ValueError("BASS-II evidence too large for bounded Gemini contract")
        snippets.append(snippet)
    return snippets
