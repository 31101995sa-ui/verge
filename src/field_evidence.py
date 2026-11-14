"""R4.2/R4.3a: Table IX source cells, QC gates, and narrow unit equivalence.

This module cannot validate physical measurements or causal claims.
Call it only with records loaded by the manifest-validated D7 loader.
"""

from __future__ import annotations

import pandas as pd

from src.flex_d7_loader import RELEASE_ID
from src.unit_rules import compare_source_quantity

REPORT_ID = "NASA/TP-2015-216046"
FIELD_RULES = {
    "oxygen_mole_fraction_raw": ("dimensionless mole fraction", None),
    "burning_rate_mm2_per_s_raw": ("mm²/s", None),
    "initial_droplet_diameter_mm_raw": ("mm", None),
    "visible_flame_extinction_diameter_mm_raw": (
        "mm", "curated_extinction_diameter_field_blocked"
    ),
    "ambient_pressure_mmhg_raw": (
        "mmHg", "curated_pressure_field_blocked"
    ),
    "burn_time_s_raw": ("s", None),
}
CLAIM_CLASSES = {"SOURCE_TRANSCRIPTION", "LIMITED_REPORTED_VALUE"}
BASE_FIELDS = {
    "flex_test_id", "source_anchor", "curated_source_anchor",
    "qc_source_anchor", "table_id", "printed_page", "pdf_page_1based",
    "qc_dap_d4_record_status", "curated_quality_status", "qc_qc_flags",
    "qc_review_reason", "qc_blocked_uses", "qc_appendix_b_anchor",
}


def verify_table_ix_numeric_claim(
    records: pd.DataFrame,
    *,
    experiment_id: str,
    raw_field: str,
    asserted_value: str,
    asserted_unit: str,
    source_anchor: str,
    claim_class: str,
    data_release_id: str = RELEASE_ID,
) -> dict:
    """Verify exact transcription or conservatively gate a reported value.

    Supports four explicitly listed raw fields. Only approved unit
    equivalences are allowed; independent physical validation is excluded.
    """
    if raw_field not in FIELD_RULES:
        raise ValueError(f"Unsupported raw field: {raw_field}")
    if claim_class not in CLAIM_CLASSES:
        raise ValueError(f"Unsupported claim class: {claim_class}")

    unit, block_column = FIELD_RULES[raw_field]
    result = {
        "data_release_id": data_release_id,
        "experiment_id": experiment_id,
        "claim_class": claim_class,
        "raw_csv_field": raw_field,
        "asserted_value": asserted_value,
        "asserted_unit": asserted_unit,
        "asserted_anchor": source_anchor,
        "source_anchor": None,
        "source_raw_value": None,
        "source_unit": unit,
        "asserted_in_source_unit": None,
        "conversion_rule": None,
        "source_qc_status": None,
        "source_qc_flags": None,
        "source_review_reason": None,
        "source_blocked_uses": None,
        "source_figure_anchor": None,
        "field_blocked": None,
        "checks": {},
        "verdict": None,
        "technical_state": "OK",
        "explanation": "",
        "scope_note": "A Table IX source cell is not independently validated physics.",
    }

    def end(verdict: str | None, reason: str, error: bool = False) -> dict:
        result["verdict"] = verdict
        result["technical_state"] = "ERROR" if error else "OK"
        result["explanation"] = reason
        return result

    if data_release_id != RELEASE_ID:
        result["checks"]["release_match"] = "FAIL"
        return end("INSUFFICIENT_EVIDENCE", "Wrong data release ID.")
    result["checks"]["release_match"] = "PASS"

    required = BASE_FIELDS | {raw_field}
    if block_column is not None:
        required.add(block_column)
    missing_columns = required - set(records.columns)
    if missing_columns or records["flex_test_id"].duplicated().any():
        result["checks"]["input_integrity"] = "ERROR"
        return end(None, f"Invalid input: missing={sorted(missing_columns)} or duplicate ID.", True)
    result["checks"]["input_integrity"] = "PASS"

    selection = records.loc[records["flex_test_id"] == experiment_id]
    if len(selection) != 1:
        result["checks"]["record_exists"] = "UNKNOWN"
        return end("INSUFFICIENT_EVIDENCE", "Record absent from the bounded D7 release.")
    row = selection.iloc[0]
    result["checks"]["record_exists"] = "PASS"

    result["source_raw_value"] = row[raw_field]
    result["source_qc_status"] = row["qc_dap_d4_record_status"]
    result["source_qc_flags"] = row["qc_qc_flags"]
    result["source_review_reason"] = row["qc_review_reason"]
    result["source_blocked_uses"] = row["qc_blocked_uses"]
    result["source_figure_anchor"] = row["qc_appendix_b_anchor"]
    flag = row[block_column] if block_column is not None else "FALSE"
    if flag not in ("TRUE", "FALSE"):
        result["checks"]["block_metadata"] = "ERROR"
        return end(None, "Unexpected field-block flag.", True)
    result["field_blocked"] = flag == "TRUE"

    canonical = (
        f"{REPORT_ID}|printed_p{row['printed_page']}|"
        f"PDF_p{row['pdf_page_1based']}|Table_IX|{experiment_id}"
    )
    source_ok = (
        row["table_id"] == "IX"
        and row["source_anchor"] == canonical
        and row["curated_source_anchor"] == canonical
        and row["qc_source_anchor"] == canonical
        and row["curated_quality_status"] == row["qc_dap_d4_record_status"]
    )
    if not source_ok:
        result["checks"]["provenance"] = "ERROR"
        return end(None, "Internal D7 source/QC mismatch.", True)
    result["source_anchor"] = canonical
    result["checks"]["provenance"] = "PASS"

    if source_anchor != canonical:
        result["checks"]["claim_locator"] = "FAIL"
        return end("INSUFFICIENT_EVIDENCE", "Claim locator does not match the source row.")
    result["checks"]["claim_locator"] = "PASS"

    raw = row[raw_field]
    if not isinstance(raw, str):
        result["checks"]["source_cell"] = "ERROR"
        return end(None, "Source cell is not a preserved text value.", True)
    if raw in ("", "–", "-"):
        result["checks"]["numeric_value"] = "UNKNOWN"
        if claim_class == "SOURCE_TRANSCRIPTION":
            # The literal dash can be transcribed, but is never a number.
            if raw == "–" and asserted_value == "–" and asserted_unit == unit:
                return end("SUPPORTED", "Table IX prints a missing-value marker, not zero.")
            return end("CONTRADICTED", f"Table IX prints {raw!r}, not a numeric {asserted_value}.")
        return end("INSUFFICIENT_EVIDENCE", "No numeric value is available for physical use.")
    result["checks"]["numeric_value"] = "PASS"

    # Field restrictions take precedence over physically usable value claims.
    if claim_class == "LIMITED_REPORTED_VALUE":
        if result["field_blocked"] or result["source_qc_status"] != "VERIFIED":
            result["checks"]["eligibility"] = "FAIL"
            return end(
                "INSUFFICIENT_EVIDENCE",
                "Value use is not approved by D7 QC; this does not negate literal transcription. "
                f"Reason: {result['source_review_reason']}",
            )
        result["checks"]["eligibility"] = "PASS"

    comparison = compare_source_quantity(
        source_text=raw,
        source_unit=unit,
        asserted_text=asserted_value,
        asserted_unit=asserted_unit,
    )
    status = comparison["status"]
    result["asserted_in_source_unit"] = comparison["asserted_in_source_unit"]
    result["conversion_rule"] = comparison["conversion_rule"]

    if status == "SOURCE_ERROR":
        result["checks"]["source_number"] = "ERROR"
        return end(None, "Malformed numerical source cell or unit.", True)
    result["checks"]["source_number"] = "PASS"

    if status == "UNSUPPORTED_UNIT":
        result["checks"]["unit_match"] = "UNKNOWN"
        return end(
            "INSUFFICIENT_EVIDENCE",
            f"Unrecognized asserted unit: {asserted_unit}.",
        )
    if status == "INCOMPATIBLE_UNIT":
        result["checks"]["unit_match"] = "FAIL"
        return end(
            "CONTRADICTED",
            f"Incompatible unit: {asserted_unit}; source unit is {unit}.",
        )
    result["checks"]["unit_match"] = "PASS"

    if status == "INVALID_ASSERTION":
        result["checks"]["claim_number"] = "UNKNOWN"
        return end("INSUFFICIENT_EVIDENCE", "Invalid claimed number.")
    result["checks"]["claim_number"] = "PASS"

    if status == "MISMATCH":
        result["checks"]["value_match"] = "FAIL"
        return end(
            "CONTRADICTED",
            f"Table IX prints {raw} {unit}; claimed {asserted_value} "
            f"{asserted_unit} converts to "
            f"{result['asserted_in_source_unit']} {unit}.",
        )

    result["checks"]["value_match"] = "PASS"
    # Retain actual printed unit even when the claim uses a conversion.
    if result["field_blocked"]:
        return end(
            "SUPPORTED",
            "Equivalent source-cell transcription only; field blocked for numerical physical use. "
            f"QC: {result['source_review_reason']}",
        )
    return end(
        "SUPPORTED",
        f"Table IX prints {raw} {unit}; asserted value is equivalent "
        "under the documented unit rule. Not physical validation.",
    )
