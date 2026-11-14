"""R5.2: bounded, deterministic NASA-EVP checks for BASS-II Table 2.1.

These verdicts apply to structured claims and this immutable D7 release only.
No free-text interpretation, physical validation, causal modelling, or FLEX pooling.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from pathlib import Path

from src.bassii_d7_loader import BASS_RELEASE_ID, BASS_REPORT_URL, load_bassii_d7

_NUMERIC = re.compile(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+))(?:±(\d+(?:\.\d*)?|\.\d+))?$")
_UNIT_FACTORS = {"mm/s": Decimal("1"), "cm/s": Decimal("10")}
_METHODS = {"EXPERIMENTAL", "COMPUTATIONAL_MODEL", "ANALYTICAL_MODEL"}

# Explicit, bounded evidence obligations: class codes are assigned by a human
# or a separately reviewed structured intake, never inferred by this verifier.
_SCOPE_RULES = {
    "GENERAL_CAUSAL_OXYGEN_EFFECT": (
        "UNQUALIFIED_CAUSAL_OXYGEN_EFFECT",
        "INSUFFICIENT_EVIDENCE",
        "The two summary rows do not establish a causal effect across all PMMA geometries.",
    ),
    "UNIVERSAL_SAFE_FLOW_THRESHOLD": (
        "UNIVERSAL_SAFE_FLOW_THRESHOLD",
        "INSUFFICIENT_EVIDENCE",
        "Thin-PMMA summary results cannot establish a universally safe flow threshold.",
    ),
    "LUNAR_HABITAT_PREDICTION": (
        "MOON_MARS_EXTRAPOLATION",
        "OUT_OF_SCOPE",
        "ISS microgravity Table 2.1 cannot predict partial-gravity lunar habitat conditions.",
    ),
    "MARS_FIRE_SUPPRESSION_CERTIFICATION": (
        "MOON_MARS_EXTRAPOLATION",
        "OUT_OF_SCOPE",
        "Table 2.1 neither validates Mars operations nor certifies fire-suppression settings.",
    ),
}


def _quantity(text: str) -> tuple[Decimal, Decimal | None] | None:
    """Parse exact decimal centers and printed ± terms without guessing errors."""
    match = _NUMERIC.fullmatch(text)
    if match is None:
        return None
    try:
        center = Decimal(match.group(1))
        spread = Decimal(match.group(2)) if match.group(2) is not None else None
    except InvalidOperation:
        return None
    if not center.is_finite() or (spread is not None and (not spread.is_finite() or spread < 0)):
        return None
    return (center, spread)


def verify_bassii_claim(release_dir: str | Path, claim: Mapping) -> dict:
    """Verify one structured BASS-II claim against a fresh manifest-checked D7.

    For source claims, values may use exact mm/s <-> cm/s conversion; a
    published experimental ± term must remain present and equivalent.
    Scope claims require an explicit scientific scope code, not NLP parsing.
    """
    result = {
        "data_release_id": BASS_RELEASE_ID,
        "report_url": BASS_REPORT_URL,
        "report_id": "NASA/TM-20210011385",
        "material_raw": None,
        "pressure_raw": None,
        "flow_configuration": None,
        "gravity_regime": None,
        "claim_class": claim.get("claim_class"),
        "oxygen_percent_condition": claim.get("o2_percent_condition"),
        "method_origin": claim.get("method_origin"),
        "scope_code": claim.get("scope_code"),
        "asserted_value_raw": claim.get("asserted_value_raw"),
        "asserted_unit": claim.get("asserted_unit"),
        "asserted_anchor": claim.get("source_anchor"),
        "source_anchor": None,
        "evidence_cell_id": None,
        "original_test_id": None,
        "source_value_raw": None,
        "source_unit": None,
        "value_kind": None,
        "experimental_uncertainty_raw": None,
        "uncertainty_status": None,
        "scientific_fitness_status": None,
        "quality_flags": None,
        "blocked_uses": None,
        "comparison_warning": None,
        "checks": {},
        "counterexamples_checked": False,
        "verdict": None,
        "technical_state": "OK",
        "explanation": "",
        "scope_note": (
            "NASA/TM-20210011385, Table 2.1, printed p.28 / PDF p.36; "
            "two summary oxygen conditions, not uniquely mapped as-run tests. "
            "Table 2.1 versus Section 2.2.5 discrepancy remains unresolved."
        ),
    }

    def finish(verdict: str | None, explanation: str, *, error: bool = False) -> dict:
        result["verdict"] = verdict
        result["technical_state"] = "ERROR" if error else "OK"
        result["explanation"] = explanation
        return result

    if claim.get("data_release_id") != BASS_RELEASE_ID:
        result["checks"]["release_match"] = "FAIL"
        return finish("INSUFFICIENT_EVIDENCE", "Claim has a missing or wrong BASS-II release ID.")
    result["checks"]["release_match"] = "PASS"

    # Fail closed for unstructured statements. A separate controlled intake
    # would have to substantiate the scope_code before this function runs.
    if "claim_text" in claim or "original_claim" in claim:
        result["checks"]["structured_input"] = "UNKNOWN"
        return finish("INSUFFICIENT_EVIDENCE", "Free text cannot be verified by this structured module.")
    if claim.get("original_test_id") not in (None, ""):
        result["checks"]["as_run_test_id"] = "FAIL"
        return finish("INSUFFICIENT_EVIDENCE", "Table 2.1 does not identify an original NASA as-run test ID.")
    kind = claim.get("claim_class")
    if kind not in {"SOURCE_TRANSCRIPTION", "SCIENTIFIC_INTERPRETATION_OR_SCOPE"}:
        result["checks"]["claim_class"] = "UNKNOWN"
        return finish("INSUFFICIENT_EVIDENCE", "Unsupported BASS-II claim class.")
    oxygen = claim.get("o2_percent_condition")
    method = claim.get("method_origin")
    if oxygen not in ("21", "16") or method not in _METHODS:
        result["checks"]["cell_identity"] = "UNKNOWN"
        return finish("INSUFFICIENT_EVIDENCE", "Unknown oxygen condition or evidence method.")
    result["checks"]["cell_identity"] = "PASS"

    # A source read or manifest failure is a technical ERROR, never a science verdict.
    try:
        cells = load_bassii_d7(release_dir)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result["checks"]["release_integrity"] = "ERROR"
        return finish(None, f"Unable to validate BASS-II D7 release: {exc}", error=True)
    result["checks"]["release_integrity"] = "PASS"

    selected = cells.loc[
        (cells["oxygen_percent_raw"] == oxygen)
        & (cells["method_origin"] == method)
    ]
    if len(selected) != 1:
        result["checks"]["cell_exists"] = "ERROR"
        return finish(None, "Validated D7 release did not resolve exactly one cell.", error=True)
    cell = selected.iloc[0]
    result["checks"]["cell_exists"] = "PASS"
    for key, column in (
        ("material_raw", "material_raw"),
        ("pressure_raw", "pressure_raw"),
        ("flow_configuration", "flow_configuration"),
        ("gravity_regime", "gravity_regime"),
        ("source_anchor", "source_anchor"),
        ("evidence_cell_id", "evidence_cell_id"),
        ("original_test_id", "original_test_id"),
        ("source_value_raw", "critical_velocity_raw"),
        ("source_unit", "critical_velocity_raw_unit"),
        ("value_kind", "value_kind"),
        ("experimental_uncertainty_raw", "experimental_uncertainty_raw"),
        ("uncertainty_status", "uncertainty_status"),
        ("scientific_fitness_status", "scientific_fitness_status"),
        ("quality_flags", "quality_flags"),
        ("blocked_uses", "qc_blocked_uses"),
        ("comparison_warning", "qc_comparison_warning"),
    ):
        result[key] = cell[column]

    if claim.get("source_anchor") != cell["source_anchor"]:
        result["checks"]["locator_match"] = "FAIL"
        return finish("INSUFFICIENT_EVIDENCE", "Claim locator does not match the exact Table 2.1 method cell.")
    result["checks"]["locator_match"] = "PASS"

    if kind == "SCIENTIFIC_INTERPRETATION_OR_SCOPE":
        scope_code = claim.get("scope_code")
        if scope_code not in _SCOPE_RULES:
            result["checks"]["scope_contract"] = "UNKNOWN"
            return finish("INSUFFICIENT_EVIDENCE", "No predefined proof obligation for this scope assertion.")
        required_block, verdict, explanation = _SCOPE_RULES[scope_code]
        if required_block not in cell["qc_blocked_uses"].split(";"):
            result["checks"]["scope_contract"] = "ERROR"
            return finish(None, "QC restriction is missing for the requested scope check.", error=True)
        result["checks"]["scope_contract"] = (
            "UNKNOWN" if verdict == "INSUFFICIENT_EVIDENCE" else "FAIL"
        )
        return finish(verdict, explanation)

    value = claim.get("asserted_value_raw")
    unit = claim.get("asserted_unit")
    if not isinstance(value, str) or not isinstance(unit, str):
        result["checks"]["quantity_input"] = "UNKNOWN"
        return finish("INSUFFICIENT_EVIDENCE", "A source-cell claim needs value and unit strings.")
    if unit not in _UNIT_FACTORS:
        if unit in {"s", "mm", "cm", "mmHg"}:
            result["checks"]["unit_match"] = "FAIL"
            return finish("CONTRADICTED", "Claim unit has an incompatible physical dimension.")
        result["checks"]["unit_match"] = "UNKNOWN"
        return finish("INSUFFICIENT_EVIDENCE", "Unknown velocity unit; no conversion is inferred.")
    result["checks"]["unit_match"] = "PASS"

    source_qty = _quantity(cell["critical_velocity_raw"])
    claimed_qty = _quantity(value)
    if source_qty is None:
        result["checks"]["source_quantity"] = "ERROR"
        return finish(None, "Invalid published numeric cell in the validated release.", error=True)
    if claimed_qty is None:
        result["checks"]["claim_quantity"] = "UNKNOWN"
        return finish("INSUFFICIENT_EVIDENCE", "Claimed value must be a decimal, optionally with ± decimal.")
    result["checks"]["source_quantity"] = "PASS"
    result["checks"]["claim_quantity"] = "PASS"

    factor = _UNIT_FACTORS[unit] / _UNIT_FACTORS[cell["critical_velocity_raw_unit"]]
    normalized = (claimed_qty[0] * factor,
                  claimed_qty[1] * factor if claimed_qty[1] is not None else None)
    result["asserted_in_source_unit"] = (
        str(normalized[0]) + ("±" + str(normalized[1]) if normalized[1] is not None else "")
    )
    result["checks"]["value_match"] = "PASS" if normalized == source_qty else "FAIL"
    if normalized != source_qty:
        return finish(
            "CONTRADICTED",
            f"Table 2.1 reports {cell['critical_velocity_raw']} mm/s for this method and O2 condition; "
            "the asserted center, uncertainty or converted unit does not match.",
        )
    return finish(
        "SUPPORTED",
        "Numerically equivalent Table 2.1 source-cell transcription only. "
        f"Method: {method}; original raw value: {cell['critical_velocity_raw']} mm/s. "
        "Not independently validated physics or a fire-safety threshold.",
    )
