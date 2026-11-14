"""R4.4 router tests; no English free-text semantic claims are asserted."""

from pathlib import Path

import pytest

from src.claim_router import verify_claim_from_release, verify_structured_claim
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release

RELEASE = Path(__file__).resolve().parents[1] / "data" / "releases" / RELEASE_ID
ANCHOR = "NASA/TP-2015-216046|printed_p20|PDF_p26|Table_IX|FLEX-002"


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE)


def test_fuel_category_provenance_supported(records):
    claim = dict(claim_class="SOURCE_TRANSCRIPTION", experiment_id="FLEX-002",
                 raw_csv_field="fuel_raw", asserted_value="Methanol", asserted_unit="category",
                 source_anchor=ANCHOR)
    result = verify_structured_claim(records, claim)
    assert result["verdict"] == "SUPPORTED"
    assert result["source_raw_value"] == "Methanol"
    assert result["source_anchor"] == ANCHOR
    assert result["source_qc_status"] == "VERIFIED"
    assert result["free_text_claim_verified"] is False


def test_source_oxygen_typo_contradicted(records):
    claim = dict(claim_class="SOURCE_TRANSCRIPTION", experiment_id="FLEX-002",
                 raw_csv_field="oxygen_mole_fraction_raw", asserted_value="0.34",
                 asserted_unit="dimensionless mole fraction", source_anchor=ANCHOR)
    assert verify_structured_claim(records, claim)["verdict"] == "CONTRADICTED"
    claim["asserted_value"] = "21"
    claim["asserted_unit"] = "%"
    assert verify_structured_claim(records, claim)["verdict"] == "SUPPORTED"


def test_burning_rate_reported_derived_source(records):
    claim = dict(claim_class="SOURCE_TRANSCRIPTION", experiment_id="FLEX-035",
                 raw_csv_field="burning_rate_mm2_per_s_raw", asserted_value="0.43",
                 asserted_unit="mm²/s",
                 source_anchor="NASA/TP-2015-216046|printed_p21|PDF_p27|Table_IX|FLEX-035")
    result = verify_structured_claim(records, claim)
    assert result["verdict"] == "SUPPORTED"
    assert result["source_raw_value"] == ".43"


def test_missing_claim_locator_abstains(records):
    claim = dict(claim_class="SOURCE_TRANSCRIPTION", experiment_id="FLEX-002",
                 raw_csv_field="fuel_raw", asserted_value="Methanol",
                 asserted_unit="category", source_anchor="wrong")
    result = verify_structured_claim(records, claim)
    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["checks"]["locator_match"] == "FAIL"


def test_unknown_claim_class_abstains(records):
    result = verify_structured_claim(records, dict(
        claim_class="FICTIONAL_PHYSICS", experiment_id="FLEX-002", source_anchor=ANCHOR))
    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["technical_state"] == "OK"


def test_not_a_free_text_verifier(records):
    claim = dict(claim_class="SOURCE_TRANSCRIPTION", experiment_id="FLEX-002",
                 raw_csv_field="fuel_raw", asserted_value="Methanol", asserted_unit="category",
                 source_anchor=ANCHOR,
                 claim_text="NASA certifies that a wooden spacecraft is fire safe")
    result = verify_structured_claim(records, claim)
    assert result["free_text_claim_verified"] is False
    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert "Free-text claims" in result["explanation"]


def test_nonexistent_release_error_no_verdict(tmp_path):
    claim = dict(claim_class="SOURCE_TRANSCRIPTION", experiment_id="FLEX-002",
                 raw_csv_field="fuel_raw", asserted_value="Methanol", asserted_unit="category",
                 source_anchor=ANCHOR)
    result = verify_claim_from_release(tmp_path, claim)
    assert result["technical_state"] == "ERROR"
    assert result["verdict"] is None
    assert result["checks"]["source_load"] == "ERROR"
