
"""R4.3b: conservative scientific scope gate for bounded FLEX D7 claims.

This accepts a *structured* claim class from the caller. It does not parse
claim text, test causality, search counterexamples, or produce physical models.
Only pass records returned by the manifest-validated D7 loader.
"""

from __future__ import annotations

import pandas as pd

from src.flex_d7_loader import RELEASE_ID

REPORT_ID = "NASA/TP-2015-216046"

# These rules are specific to the current D6/D7 bounded sample.
SCOPE_RULES = {
    "CAUSAL_EFFECT": (
        "INSUFFICIENT_EVIDENCE",
        "No controlled comparability review supports a causal effect across these selected records.",
    ),
    "EXPERIMENTAL_THRESHOLD": (
        "INSUFFICIENT_EVIDENCE",
        "The selected records do not establish a validated general experimental threshold.",
    ),
    "MOON_MARS_EXTRAPOLATION": (
        "OUT_OF_SCOPE",
        "FLEX ISS microgravity records cannot validate partial-gravity predictions.",
    ),
    "CERTIFIED_SAFE": (
        "OUT_OF_SCOPE",
        "These FLEX droplet experiments cannot certify spacecraft materials or hardware as fire safe.",
    ),
    "FIRE_RISK_SCORE": (
        "OUT_OF_SCOPE",
        "This release does not provide validated fire-risk scores or safety ratings.",
    ),
}

REQUIRED_COLUMNS = {
    "flex_test_id", "source_anchor", "curated_source_anchor",
    "qc_source_anchor", "table_id", "printed_page", "pdf_page_1based",
    "qc_dap_d4_record_status", "curated_quality_status",
    "qc_qc_flags", "qc_review_reason", "qc_blocked_uses",
}


def evaluate_claim_scope(
    records: pd.DataFrame,
    *,
    experiment_id: str,
    claim_class: str,
    source_anchor: str,
    data_release_id: str = RELEASE_ID,
) -> dict:
    """Apply conservative D7 scope restrictions to a classified claim.

    Not a natural-language classifier; caller is responsible for assigning
    a correct claim class. No SUPPORTED/CONTRADICTED verdict can be issued.
    """
    if claim_class not in SCOPE_RULES:
        raise ValueError(f"Unsupported scope claim class: {claim_class}")

    result = {
        "data_release_id": data_release_id,
        "claim_class": claim_class,
        "experiment_id": experiment_id,
        "asserted_anchor": source_anchor,
        "source_anchor": None,
        "report_id": REPORT_ID,
        "printed_page": None,
        "pdf_page_1based": None,
        "source_qc_status": None,
        "source_qc_flags": None,
        "source_review_reason": None,
        "source_blocked_uses": None,
        "checks": {},
        "counterexamples_checked": False,
        "verdict": None,
        "technical_state": "OK",
        "explanation": "",
        "scope_note": (
            "Policy decision for the 17-record FLEX D7 sample; "
            "not a counterexample search or independent physical test."
        ),
    }

    def finish(
        verdict: str | None,
        explanation: str,
        error: bool = False,
    ) -> dict:
        result["verdict"] = verdict
        result["technical_state"] = "ERROR" if error else "OK"
        result["explanation"] = explanation
        return result

    if data_release_id != RELEASE_ID:
        result["checks"]["release_match"] = "FAIL"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Unknown or mismatched D7 release.",
        )
    result["checks"]["release_match"] = "PASS"

    missing = REQUIRED_COLUMNS - set(records.columns)
    if missing:
        result["checks"]["input_integrity"] = "ERROR"
        return finish(
            None,
            f"Missing required D7 columns: {sorted(missing)}",
            True,
        )

    ids = records["flex_test_id"]
    if ids.isna().any() or ids.eq("").any() or ids.duplicated().any():
        result["checks"]["input_integrity"] = "ERROR"
        return finish(
            None,
            "Missing or duplicate FLEX experiment IDs.",
            True,
        )
    result["checks"]["input_integrity"] = "PASS"

    matches = records.loc[ids == experiment_id]
    if len(matches) != 1:
        result["checks"]["record_exists"] = "UNKNOWN"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Experiment is absent from this bounded D7 release.",
        )
    result["checks"]["record_exists"] = "PASS"
    row = matches.iloc[0]

    result["source_qc_status"] = row["qc_dap_d4_record_status"]
    result["source_qc_flags"] = row["qc_qc_flags"]
    result["source_review_reason"] = row["qc_review_reason"]
    result["source_blocked_uses"] = row["qc_blocked_uses"]
    result["printed_page"] = row["printed_page"]
    result["pdf_page_1based"] = row["pdf_page_1based"]

    canonical = (
        f"{REPORT_ID}|printed_p{row['printed_page']}|"
        f"PDF_p{row['pdf_page_1based']}|Table_IX|{experiment_id}"
    )
    consistent = (
        row["table_id"] == "IX"
        and row["source_anchor"] == canonical
        and row["curated_source_anchor"] == canonical
        and row["qc_source_anchor"] == canonical
        and row["curated_quality_status"] == row["qc_dap_d4_record_status"]
    )
    if not consistent:
        result["checks"]["source_integrity"] = "ERROR"
        return finish(
            None,
            "Inconsistent D7 Table IX or QC provenance.",
            True,
        )
    result["checks"]["source_integrity"] = "PASS"
    result["source_anchor"] = canonical

    if source_anchor != canonical:
        result["checks"]["locator_match"] = "FAIL"
        return finish(
            "INSUFFICIENT_EVIDENCE",
            "Claim locator does not match the audited Table IX row.",
        )
    result["checks"]["locator_match"] = "PASS"

    verdict, explanation = SCOPE_RULES[claim_class]
    result["checks"]["scope_gate"] = (
        "UNKNOWN" if verdict == "INSUFFICIENT_EVIDENCE" else "FAIL"
    )
    return finish(verdict, explanation)
