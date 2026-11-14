"""R4.4: route *structured* FLEX D7 claims to deterministic checks.

A claim's English prose is NOT parsed or independently checked here. Callers
must create truthful structured inputs from that prose; do not expose this as
free-text verification. Scores from R3 have no influence on verdicts.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import pandas as pd

from src.field_evidence import FIELD_RULES, verify_table_ix_numeric_claim
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.scope_gate import SCOPE_RULES, evaluate_claim_scope

REPORT_ID = "NASA/TP-2015-216046"
REPORT_URL = "https://ntrs.nasa.gov/citations/20150023456"


def _unresolved(claim: Mapping, explanation: str, *, technical_error=False) -> dict:
    return {
        "claim_class": claim.get("claim_class"),
        "experiment_id": claim.get("experiment_id"),
        "data_release_id": claim.get("data_release_id", RELEASE_ID),
        "raw_csv_field": claim.get("raw_csv_field"),
        "asserted_value": claim.get("asserted_value"),
        "asserted_unit": claim.get("asserted_unit"),
        "source_anchor": None,
        "source_raw_value": None,
        "source_unit": None,
        "source_qc_status": None,
        "source_qc_flags": None,
        "source_review_reason": None,
        "source_blocked_uses": None,
        "checks": {},
        "verdict": None if technical_error else "INSUFFICIENT_EVIDENCE",
        "technical_state": "ERROR" if technical_error else "OK",
        "explanation": explanation,
        "structured_claim_only": True,
        "free_text_claim_verified": False,
    }


def _verify_fuel_literal(records: pd.DataFrame, claim: Mapping) -> dict:
    """Compare a single literal NASA fuel category after provenance checks."""
    result = _unresolved(claim, "Claim not evaluated")
    required = {
        "flex_test_id", "fuel_raw", "source_anchor", "curated_source_anchor",
        "qc_source_anchor", "table_id", "printed_page", "pdf_page_1based",
        "qc_dap_d4_record_status", "curated_quality_status", "qc_qc_flags",
        "qc_review_reason", "qc_blocked_uses",
    }
    missing = required - set(records.columns)
    if missing or records["flex_test_id"].isna().any() or records["flex_test_id"].eq("").any() or records["flex_test_id"].duplicated().any():
        result["checks"]["input_integrity"] = "ERROR"
        result.update(verdict=None, technical_state="ERROR", explanation=f"Invalid D7 source structure: {sorted(missing)}")
        return result
    result["checks"]["input_integrity"] = "PASS"
    if claim.get("data_release_id", RELEASE_ID) != RELEASE_ID:
        result["checks"]["release_match"] = "FAIL"
        result["explanation"] = "Data release ID does not match the bounded D7 release."
        return result
    result["checks"]["release_match"] = "PASS"
    selection = records.loc[records["flex_test_id"] == claim.get("experiment_id")]
    if len(selection) != 1:
        result["checks"]["record_exists"] = "UNKNOWN"
        result["explanation"] = "Experiment is not present in the D7 sample."
        return result
    row = selection.iloc[0]
    result["checks"]["record_exists"] = "PASS"
    result["source_raw_value"] = row["fuel_raw"]
    result["source_unit"] = "category"
    result["source_qc_status"] = row["qc_dap_d4_record_status"]
    result["source_qc_flags"] = row["qc_qc_flags"]
    result["source_review_reason"] = row["qc_review_reason"]
    result["source_blocked_uses"] = row["qc_blocked_uses"]
    canonical = (
        f"{REPORT_ID}|printed_p{row['printed_page']}|"
        f"PDF_p{row['pdf_page_1based']}|Table_IX|{claim['experiment_id']}"
    )
    if not (
        row["table_id"] == "IX"
        and row["source_anchor"] == canonical
        and row["curated_source_anchor"] == canonical
        and row["qc_source_anchor"] == canonical
        and row["curated_quality_status"] == row["qc_dap_d4_record_status"]
    ):
        result["checks"]["source_integrity"] = "ERROR"
        result.update(verdict=None, technical_state="ERROR", explanation="D7 provenance or QC mismatch")
        return result
    result["checks"]["source_integrity"] = "PASS"
    result["source_anchor"] = canonical
    if claim.get("source_anchor") != canonical:
        result["checks"]["locator_match"] = "FAIL"
        result["explanation"] = "Claim locator does not match the audited source."
        return result
    result["checks"]["locator_match"] = "PASS"
    if claim.get("asserted_unit") != "category":
        result["checks"]["unit_match"] = "FAIL"
        result["verdict"] = "CONTRADICTED"
        result["explanation"] = "Fuel is reported as a category, not as a numerical unit."
        return result
    result["checks"]["unit_match"] = "PASS"
    if not isinstance(row["fuel_raw"], str) or not row["fuel_raw"]:
        result["checks"]["source_cell"] = "ERROR"
        result.update(verdict=None, technical_state="ERROR", explanation="Malformed categorical source cell")
        return result
    if claim.get("asserted_value") != row["fuel_raw"]:
        result["checks"]["value_match"] = "FAIL"
        result["verdict"] = "CONTRADICTED"
        result["explanation"] = f"Table IX prints {row['fuel_raw']!r} as the fuel."
        return result
    result["checks"]["value_match"] = "PASS"
    result["verdict"] = "SUPPORTED"
    result["explanation"] = "The specified Table IX fuel category is transcribed correctly."
    return result


def verify_structured_claim(records: pd.DataFrame, claim: Mapping) -> dict:
    """Dispatch narrow, explicitly classified assertions; never trust R3 rank."""
    if "claim_text" in claim or "claim_text_en" in claim:
        return _unresolved(
            claim, "Free-text claims are not evaluated; supply only structured assertions."
        )

    kind = claim.get("claim_class")
    experiment_id = claim.get("experiment_id")
    anchor = claim.get("source_anchor")
    release = claim.get("data_release_id", RELEASE_ID)

    if not isinstance(kind, str) or not isinstance(experiment_id, str) or not isinstance(anchor, str):
        return _unresolved(claim, "Missing or invalid mandatory structured claim fields.")

    if kind in SCOPE_RULES:
        answer = evaluate_claim_scope(
            records, experiment_id=experiment_id,
            claim_class=kind, source_anchor=anchor, data_release_id=release,
        )
    elif kind in ("SOURCE_TRANSCRIPTION", "LIMITED_REPORTED_VALUE"):
        field = claim.get("raw_csv_field")
        if kind == "SOURCE_TRANSCRIPTION" and field == "fuel_raw":
            answer = _verify_fuel_literal(records, claim)
        elif field in FIELD_RULES:
            if not isinstance(claim.get("asserted_value"), str) or not isinstance(claim.get("asserted_unit"), str):
                return _unresolved(claim, "Numeric claim requires asserted_value and asserted_unit strings.")
            answer = verify_table_ix_numeric_claim(
                records, experiment_id=experiment_id, raw_field=field,
                asserted_value=claim["asserted_value"],
                asserted_unit=claim["asserted_unit"], source_anchor=anchor,
                claim_class=kind, data_release_id=release,
            )
        else:
            return _unresolved(claim, f"Unsupported source field for this claim class: {field!r}.")
    else:
        return _unresolved(claim, f"Claim class has no implemented proof rules: {kind!r}.")

    answer["report_url"] = REPORT_URL
    answer["structured_claim_only"] = True
    answer["free_text_claim_verified"] = False
    answer["raw_csv_field"] = claim.get("raw_csv_field")
    answer["asserted_value"] = claim.get("asserted_value")
    answer["asserted_unit"] = claim.get("asserted_unit")
    return answer


def verify_claim_from_release(release_dir: str | Path, claim: Mapping) -> dict:
    """Validate the manifest and CSV bytes before running the claim router."""
    try:
        records = load_flex_d7_release(release_dir)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = _unresolved(claim, f"D7 release loading failed: {type(exc).__name__}: {exc}", technical_error=True)
        result["checks"]["source_load"] = "ERROR"
        result["structured_claim_only"] = True
        result["free_text_claim_verified"] = False
        return result
    return verify_structured_claim(records, claim)
