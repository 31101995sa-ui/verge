"""R5.2: BASS-II claims are checked independently against immutable D7."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from benchmarks.run_bassii_benchmark import RELEASE, run_benchmark, structured_case
from src.bassii_d7_loader import BASS_RELEASE_ID, load_bassii_d7
from src.bassii_evp import verify_bassii_claim


def _claim(o2: str = "21", method: str = "EXPERIMENTAL", value: str = "10±5", unit: str = "mm/s") -> dict:
    cells = load_bassii_d7(RELEASE)
    cell = cells.loc[
        (cells["oxygen_percent_raw"] == o2)
        & (cells["method_origin"] == method)
    ].iloc[0]
    return {
        "data_release_id": BASS_RELEASE_ID,
        "claim_class": "SOURCE_TRANSCRIPTION",
        "o2_percent_condition": o2,
        "method_origin": method,
        "asserted_value_raw": value,
        "asserted_unit": unit,
        "source_anchor": cell["source_anchor"],
    }


def test_pre_registered_ten_cases_are_independently_executed():
    result = run_benchmark()
    assert result["cases_total"] == 10
    assert result["cases_passed"] == 10
    assert all(item["passed"] for item in result["observations"])
    assert result["observations"][0]["evidence"]["source_value_raw"] == "10±5"
    assert result["observations"][3]["evidence"]["value_kind"] == "DERIVED"
    assert "expected_scientific_verdict" not in result["observations"][0]["input"]


def test_experimental_spread_cannot_be_dropped():
    output = verify_bassii_claim(RELEASE, _claim(value="10"))
    assert output["verdict"] == "CONTRADICTED"
    assert output["experimental_uncertainty_raw"] == "±5"


def test_exact_conversion_of_experimental_spread():
    output = verify_bassii_claim(RELEASE, _claim(value="1±0.5", unit="cm/s"))
    assert output["verdict"] == "SUPPORTED"
    assert output["asserted_in_source_unit"] == "10±5.0"


def test_model_has_unreported_uncertainty_not_zero():
    output = verify_bassii_claim(RELEASE, _claim(method="COMPUTATIONAL_MODEL", value="15"))
    assert output["verdict"] == "SUPPORTED"
    assert output["experimental_uncertainty_raw"] == ""
    assert output["uncertainty_status"] == "NOT_REPORTED"
    wrong = verify_bassii_claim(RELEASE, _claim(method="COMPUTATIONAL_MODEL", value="15±0"))
    assert wrong["verdict"] == "CONTRADICTED"


def test_wrong_method_source_anchor_abstains():
    claim = _claim(method="COMPUTATIONAL_MODEL", value="15")
    claim["method_origin"] = "ANALYTICAL_MODEL"
    output = verify_bassii_claim(RELEASE, claim)
    assert output["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert output["checks"]["locator_match"] == "FAIL"


def test_unknown_source_cell_no_made_up_test_id():
    claim = _claim()
    claim["o2_percent_condition"] = "17"
    output = verify_bassii_claim(RELEASE, claim)
    assert output["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert output["evidence_cell_id"] is None


def test_scope_without_human_review_code_abstains():
    claim = _claim()
    claim["claim_class"] = "SCIENTIFIC_INTERPRETATION_OR_SCOPE"
    output = verify_bassii_claim(RELEASE, claim)
    assert output["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert output["checks"]["scope_contract"] == "UNKNOWN"


def test_unstructured_text_is_not_processed():
    claim = _claim()
    claim["claim_text"] = "NASA proved PMMA is safe"
    output = verify_bassii_claim(RELEASE, claim)
    assert output["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert output["source_value_raw"] is None


def test_wrong_release_cannot_be_supported():
    claim = _claim()
    claim["data_release_id"] = "FLEX-R1-SAMPLE-20261114-v1.0"
    output = verify_bassii_claim(RELEASE, claim)
    assert output["verdict"] == "INSUFFICIENT_EVIDENCE"


def test_corrupted_manifest_payload_is_technical_error(tmp_path):
    target = tmp_path / "release"
    shutil.copytree(RELEASE, target)
    with (target / "BASS_II_R5_D7_curated_6cells_v1.csv").open("ab") as handle:
        handle.write(b"INVALID_MODIFICATION")
    output = verify_bassii_claim(target, _claim())
    assert output["verdict"] is None
    assert output["technical_state"] == "ERROR"
    assert output["checks"]["release_integrity"] == "ERROR"


def test_original_release_is_not_modified():
    path = RELEASE / "BASS_II_R5_D7_raw_2rows_v1.csv"
    before = path.read_bytes()
    verify_bassii_claim(RELEASE, _claim())
    assert path.read_bytes() == before


def test_scope_codes_keep_separate_verdicts():
    claim = _claim()
    claim["claim_class"] = "SCIENTIFIC_INTERPRETATION_OR_SCOPE"
    for scope, expected in [
        ("GENERAL_CAUSAL_OXYGEN_EFFECT", "INSUFFICIENT_EVIDENCE"),
        ("UNIVERSAL_SAFE_FLOW_THRESHOLD", "INSUFFICIENT_EVIDENCE"),
        ("LUNAR_HABITAT_PREDICTION", "OUT_OF_SCOPE"),
        ("MARS_FIRE_SUPPRESSION_CERTIFICATION", "OUT_OF_SCOPE"),
    ]:
        claim["scope_code"] = scope
        output = verify_bassii_claim(RELEASE, claim)
        assert output["verdict"] == expected
        assert output["counterexamples_checked"] is False


def test_fabricated_nasa_as_run_id_is_not_accepted():
    claim = _claim()
    claim["original_test_id"] = "BASS-II-TEST-021"
    output = verify_bassii_claim(RELEASE, claim)
    assert output["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert output["checks"]["as_run_test_id"] == "FAIL"
