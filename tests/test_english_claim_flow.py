"""R4.8: English candidate confirmation must not bypass source verification."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.claim_text_parser import parse_table_ix_claim
from src.english_claim_flow import verify_confirmed_english_claim
from src.evidence_ledger import ledger_as_json, make_evidence_entry
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release

RELEASE = Path(__file__).resolve().parents[1] / "data" / "releases" / RELEASE_ID
TIME = datetime(2026, 11, 14, 10, 0, tzinfo=timezone.utc)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE)


@pytest.mark.parametrize("sentence,verdict", [
    ("NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002.", "SUPPORTED"),
    ("NASA Table IX lists an oxygen mole fraction of 0.34 for FLEX-002.", "CONTRADICTED"),
    ("NASA Table IX lists an initial droplet diameter of 0.186 cm for FLEX-002.", "SUPPORTED"),
    ("NASA Table IX prints 2 mm as the visible-flame extinction droplet diameter for FLEX-034.", "SUPPORTED"),
])
def test_confirmed_text_routes_to_manifest_verifier(records, sentence, verdict):
    candidate = parse_table_ix_claim(sentence, records)["claim"]
    result = verify_confirmed_english_claim(
        records, RELEASE, original_text=sentence, candidate=candidate
    )
    assert result["verdict"] == verdict
    assert result["technical_state"] == "OK"
    assert result["source_anchor"].endswith(candidate["experiment_id"])


def test_tampered_candidate_cannot_be_confirmed(records):
    sentence = "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002."
    candidate = parse_table_ix_claim(sentence, records)["claim"].copy()
    candidate["asserted_value"] = "0.34"
    with pytest.raises(ValueError, match="stale, or modified"):
        verify_confirmed_english_claim(records, RELEASE, original_text=sentence, candidate=candidate)


def test_changed_text_cannot_confirm_stale_candidate(records):
    first = "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002."
    changed = "NASA Table IX lists an oxygen mole fraction of 0.34 for FLEX-002."
    candidate = parse_table_ix_claim(first, records)["claim"]
    with pytest.raises(ValueError, match="stale, or modified"):
        verify_confirmed_english_claim(records, RELEASE, original_text=changed, candidate=candidate)


def test_general_physical_claim_cannot_be_passed_as_source_claim(records):
    sentence = "FLEX-034 has a scientifically validated extinction droplet diameter of 2 mm."
    candidate = {
        "data_release_id": RELEASE_ID,
        "claim_class": "SOURCE_TRANSCRIPTION",
        "experiment_id": "FLEX-034",
        "raw_csv_field": "visible_flame_extinction_diameter_mm_raw",
        "asserted_value": "2",
        "asserted_unit": "mm",
        "source_anchor": records.loc[records.flex_test_id == "FLEX-034", "source_anchor"].iloc[0],
    }
    with pytest.raises(ValueError, match="Unconfirmed"):
        verify_confirmed_english_claim(records, RELEASE, original_text=sentence, candidate=candidate)


def test_original_text_retained_in_export_but_not_verifier_input(records):
    text = "NASA Table IX lists an oxygen mole fraction of 0.34 for FLEX-002."
    candidate = parse_table_ix_claim(text, records)["claim"]
    assert "claim_text" not in candidate
    result = verify_confirmed_english_claim(records, RELEASE, original_text=text, candidate=candidate)
    entry = make_evidence_entry(candidate, result, sequence=1, claim_text=text, recorded_at=TIME)
    exported = json.loads(ledger_as_json([entry]))
    saved = exported["entries"][0]
    assert saved["claim_text"] == text
    assert saved["claim"]["asserted_value"] == "0.34"
    assert saved["evaluation"]["source_raw_value"] == ".21"
    assert saved["verdict"] == "CONTRADICTED"
    assert saved["counterexamples_checked"] is False
    assert saved["generation_model_used"] is None


def test_text_changes_ledger_fingerprint_for_same_structured_claim(records):
    first_text = "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002."
    second_text = " nasa table ix lists an oxygen mole fraction of 0.21 for flex-002. "
    candidate = parse_table_ix_claim(first_text, records)["claim"]
    result = verify_confirmed_english_claim(records, RELEASE, original_text=first_text, candidate=candidate)
    first = make_evidence_entry(candidate, result, sequence=1, claim_text=first_text, recorded_at=TIME)
    second = make_evidence_entry(candidate, result, sequence=1, claim_text=second_text, recorded_at=TIME)
    assert first["entry_id"] != second["entry_id"]
    assert first["claim"] == second["claim"]


def test_bad_ledger_text_rejected(records):
    text = "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002."
    claim = parse_table_ix_claim(text, records)["claim"]
    result = verify_confirmed_english_claim(records, RELEASE, original_text=text, candidate=claim)
    with pytest.raises(ValueError, match="claim_text"):
        make_evidence_entry(claim, result, sequence=1, claim_text=" ")
