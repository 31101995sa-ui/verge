
"""R4.1: bounded Table IX oxygen-cell verification (not physical validation)."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

import pandas as pd

from src.flex_d7_loader import RELEASE_ID


REPORT_ID = "NASA/TP-2015-216046"
RAW_FIELD = "oxygen_mole_fraction_raw"
SOURCE_UNIT = "dimensionless mole fraction"

REQUIRED_FIELDS = {
    "flex_test_id",
    RAW_FIELD,
    "source_anchor",
    "curated_source_anchor",
    "qc_source_anchor",
    "table_id",
    "printed_page",
    "pdf_page_1based",
    "qc_dap_d4_record_status",
    "curated_quality_status",
    "qc_qc_flags",
    "qc_review_reason",
    "qc_permitted_uses",
    "qc_blocked_uses",
}


def verify_oxygen_transcription(
    records: pd.DataFrame,
    *,
    experiment_id: str,
    asserted_value: str,
    asserted_unit: str,
    source_anchor: str,
    data_release_id: str = RELEASE_ID,
) -> dict:
    """Check one structured claim: Table IX prints O2 mole fraction X.

    Caller must supply records from the manifest-validated D7 loader.
    This does not validate physical/causal conclusions.
    """

    result = {
        "claim_class": "SOURCE_TRANSCRIPTION",
        "data_release_id": data_release_id,
        "experiment_id": experiment_id,
        "raw_csv_field": RAW_FIELD,
        "asserted_value": asserted_value,
        "asserted_unit": asserted_unit,
        "source_unit": SOURCE_UNIT,
        "source_anchor": source_anchor,
        "source_raw_value": None,
        "source_qc_status": None,
        "source_qc_flags": None,
        "source_review_reason": None,
        "source_permitted_uses": None,
        "source_blocked_uses": None,
        "checks": {},
        "verdict": None,
        "technical_state": "OK",
        "explanation": "",
        "scope_note": (
            "Table IX text only; not physical validity or causality."
        ),
    }

    def finish(
        verdict: str | None,
        note: str,
        *,
        error: bool = False,
    ) -> dict:
        result["verdict"] = verdict
        result["technical_state"] = "ERROR" if error else "OK"
        result["explanation"] = note
        return result

    if data_release_id != RELEASE_ID:
        result["checks"]["release_match"] = "FAIL"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Requested release is not D7 v1.0.",
        )

    result["checks"]["release_match"] = "PASS"

    missing = REQUIRED_FIELDS - set(records.columns)

    if missing or records["flex_test_id"].duplicated().any():
        result["checks"]["data_integrity"] = "ERROR"
        return finish(
            None,
            f"Invalid D7 input (missing={sorted(missing)} "
            "or duplicate IDs).",
            error=True,
        )

    result["checks"]["data_integrity"] = "PASS"

    selection = records.loc[
        records["flex_test_id"] == experiment_id
    ]

    if len(selection) != 1:
        result["checks"]["record_exists"] = "UNKNOWN"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Experiment not found in the bounded D7 release.",
        )

    result["checks"]["record_exists"] = "PASS"
    row = selection.iloc[0]

    # Preserve original NASA text and Stellar Anvil QC metadata.
    result["source_raw_value"] = row[RAW_FIELD]
    result["source_qc_status"] = row["qc_dap_d4_record_status"]
    result["source_qc_flags"] = row["qc_qc_flags"]
    result["source_review_reason"] = row["qc_review_reason"]
    result["source_permitted_uses"] = row["qc_permitted_uses"]
    result["source_blocked_uses"] = row["qc_blocked_uses"]

    canonical_anchor = (
        f"{REPORT_ID}|printed_p{row['printed_page']}|"
        f"PDF_p{row['pdf_page_1based']}|"
        f"Table_IX|{experiment_id}"
    )

    anchors_agree = (
        row["table_id"] == "IX"
        and row["source_anchor"] == canonical_anchor
        and row["curated_source_anchor"] == canonical_anchor
        and row["qc_source_anchor"] == canonical_anchor
        and row["curated_quality_status"]
        == row["qc_dap_d4_record_status"]
    )

    if not anchors_agree:
        result["checks"]["source_integrity"] = "ERROR"
        return finish(
            None,
            "Source/QC provenance mismatch.",
            error=True,
        )

    result["checks"]["source_integrity"] = "PASS"

    if not source_anchor or source_anchor != canonical_anchor:
        result["checks"]["locator_match"] = "FAIL"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Claim locator is missing or does not match Table IX.",
        )

    result["checks"]["locator_match"] = "PASS"

    raw = row[RAW_FIELD]

    if raw in ("", "–", "-"):
        result["checks"]["numeric_value_present"] = "UNKNOWN"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Table IX has no numeric oxygen value for this record.",
        )

    result["checks"]["numeric_value_present"] = "PASS"

    try:
        reported = Decimal(raw)
    except (InvalidOperation, ValueError):
        result["checks"]["source_number"] = "ERROR"
        return finish(
            None,
            "Cannot parse source oxygen value as Decimal.",
            error=True,
        )

    if asserted_unit != SOURCE_UNIT:
        result["checks"]["unit_match"] = "FAIL"
        return finish(
            "CONTRADICTED",
            f"Source unit is {SOURCE_UNIT}, not {asserted_unit}.",
        )

    result["checks"]["unit_match"] = "PASS"

    try:
        asserted = Decimal(asserted_value)
    except (InvalidOperation, ValueError, TypeError):
        result["checks"]["number_parse"] = "UNKNOWN"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Claimed value is not a valid decimal number.",
        )

    if not reported.is_finite() or not asserted.is_finite():
        result["checks"]["number_parse"] = "UNKNOWN"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Non-finite input is not a valid Table IX claim.",
        )

    result["checks"]["number_parse"] = "PASS"

    if asserted != reported:
        result["checks"]["value_match"] = "FAIL"
        return finish(
            "CONTRADICTED",
            f"Table IX prints {raw} ({SOURCE_UNIT}); "
            f"claimed {asserted_value}.",
        )

    result["checks"]["value_match"] = "PASS"

    return finish(
        "SUPPORTED",
        "Exact bounded Table IX oxygen-cell transcription "
        "is supported; no physical inference.",
    )
