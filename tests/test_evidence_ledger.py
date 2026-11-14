"""R4.6: actual source-linked verifier responses can be exported safely."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.claim_router import verify_claim_from_release
from src.evidence_ledger import ledger_as_json, make_evidence_entry
from src.flex_d7_loader import RELEASE_ID

RELEASE = Path(__file__).resolve().parents[1] / "data" / "releases" / RELEASE_ID
ANCHOR_002 = "NASA/TP-2015-216046|printed_p20|PDF_p26|Table_IX|FLEX-002"
ANCHOR_034 = "NASA/TP-2015-216046|printed_p21|PDF_p27|Table_IX|FLEX-034"
TIME = datetime(2026, 11, 14, 8, 30, tzinfo=timezone.utc)


def make_claim(value="0.21", *, experiment="FLEX-002", claim_class="SOURCE_TRANSCRIPTION", raw_field="oxygen_mole_fraction_raw", unit="dimensionless mole fraction", anchor=ANCHOR_002):
    return {
        "data_release_id": RELEASE_ID,
        "claim_class": claim_class,
        "experiment_id": experiment,
        "raw_csv_field": raw_field,
        "asserted_value": value,
        "asserted_unit": unit,
        "source_anchor": anchor,
    }


def observed_entry(claim, sequence=1):
    result = verify_claim_from_release(RELEASE, claim)
    return make_evidence_entry(claim, result, sequence=sequence, recorded_at=TIME)


def test_supported_source_cell_preserved_with_qc():
    entry = observed_entry(make_claim())
    assert entry["evaluation"]["verdict"] == "SUPPORTED"
    assert entry["evaluation"]["source_raw_value"] == ".21"
    assert entry["evaluation"]["source_anchor"] == ANCHOR_002
    assert entry["evaluation"]["source_qc_status"] == "VERIFIED"
    assert entry["evaluation"]["checks"]["value_match"] == "PASS"
    assert entry["claim_text"] is None
    assert entry["counterexamples_checked"] is False
    assert entry["verifier_version"] == "R4.4/R4.5 deterministic v0.1"
    assert entry["source_refs"] == [ANCHOR_002]


def test_deliberately_wrong_number_in_export():
    entry = observed_entry(make_claim("0.34"))
    assert entry["evaluation"]["verdict"] == "CONTRADICTED"
    assert entry["evaluation"]["source_raw_value"] == ".21"
    assert entry["claim"]["asserted_value"] == "0.34"
    assert entry["evaluation"]["checks"]["value_match"] == "FAIL"


def test_blocked_physical_claim_stays_unresolved():
    entry = observed_entry(make_claim("2", experiment="FLEX-034", claim_class="LIMITED_REPORTED_VALUE", raw_field="visible_flame_extinction_diameter_mm_raw", unit="mm", anchor=ANCHOR_034))
    assert entry["evaluation"]["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert entry["evaluation"]["field_blocked"] is True
    assert entry["evaluation"]["source_raw_value"] == "2"


def test_scope_claim_preserves_out_of_scope_and_locator():
    entry = observed_entry(make_claim(None, claim_class="MOON_MARS_EXTRAPOLATION", raw_field=None, unit=None))
    assert entry["evaluation"]["verdict"] == "OUT_OF_SCOPE"
    assert entry["evaluation"]["source_anchor"] == ANCHOR_002


def test_export_contains_complete_entries_not_expected_answers():
    first = observed_entry(make_claim("0.21"), sequence=1)
    second = observed_entry(make_claim("0.34"), sequence=2)
    exported = json.loads(ledger_as_json([first, second]))
    assert exported["entry_count"] == 2
    assert exported["data_release_id"] == RELEASE_ID
    assert exported["entries"][0]["evaluation"]["verdict"] == "SUPPORTED"
    assert exported["entries"][1]["evaluation"]["verdict"] == "CONTRADICTED"
    assert "expected_verdict" not in exported["entries"][0]


def test_entry_fingerprint_is_deterministic_with_fixed_timestamp():
    assert observed_entry(make_claim())["entry_id"] == observed_entry(make_claim())["entry_id"]


def test_repeated_claims_get_unique_sequence_ids():
    first = observed_entry(make_claim(), sequence=1)
    second = observed_entry(make_claim(), sequence=2)
    assert first["entry_id"] != second["entry_id"]


def test_entry_does_not_mutate_claim_or_verifier_result():
    claim = make_claim()
    result = verify_claim_from_release(RELEASE, claim)
    original_claim = dict(claim)
    original_result = json.loads(json.dumps(result))
    entry = make_evidence_entry(claim, result, sequence=1, recorded_at=TIME)
    entry["evaluation"]["checks"]["value_match"] = "CHANGED"
    assert claim == original_claim
    assert result == original_result


def test_technical_error_cannot_carry_scientific_verdict():
    claim = make_claim()
    with pytest.raises(ValueError, match="Invalid separation"):
        make_evidence_entry(
            claim, {"technical_state": "ERROR", "verdict": "SUPPORTED"},
            sequence=1, recorded_at=TIME,
        )


def test_technical_error_with_none_verdict_is_recorded():
    claim = make_claim()
    entry = make_evidence_entry(
        claim, {"technical_state": "ERROR", "verdict": None, "checks": {"source_load": "ERROR"}},
        sequence=1, recorded_at=TIME,
    )
    assert entry["evaluation"]["verdict"] is None
    assert entry["evaluation"]["technical_state"] == "ERROR"


def test_naive_time_refused():
    with pytest.raises(ValueError, match="timezone"):
        make_evidence_entry(
            make_claim(), {"technical_state": "OK", "verdict": "SUPPORTED"},
            sequence=1, recorded_at=datetime(2026, 11, 14),
        )


def test_invalid_sequence_refused():
    with pytest.raises(ValueError, match="sequence"):
        make_evidence_entry(
            make_claim(), {"technical_state": "OK", "verdict": "SUPPORTED"},
            sequence=0, recorded_at=TIME,
        )


def test_evp_fields_present_in_ledger():
    entry = observed_entry(make_claim())
    assert {"run_id", "claim_id", "claim_text", "proof_obligation", "check_results",
            "counterexamples_checked", "verdict", "domain_limits", "generation_model_used",
            "verifier_version", "timestamp_utc", "human_review_note"}.issubset(entry)
    assert entry["proof_obligation"] == "SOURCE_TRANSCRIPTION"
    assert entry["human_review_note"] is None
