"""R5.3: BASS-II source claim intake and session ledger integrity."""

from datetime import datetime, timezone
import json
from pathlib import Path

import pandas as pd
import pytest

from src.bassii_d7_loader import BASS_RELEASE_ID, load_bassii_d7
from src.bassii_evp import verify_bassii_claim
from src.bassii_ledger import SCHEMA, bassii_ledger_as_json, make_bassii_entry
from src.bassii_verification_ui import build_bassii_source_claim
from src.i18n import tr

RELEASE = Path(__file__).resolve().parents[1] / "data" / "releases" / BASS_RELEASE_ID


@pytest.fixture
def cells():
    return load_bassii_d7(RELEASE)


def _claim(cells, oxygen="21", method="EXPERIMENTAL", value="10±5", unit="mm/s"):
    selected = cells.loc[
        (cells["oxygen_percent_raw"] == oxygen)
        & (cells["method_origin"] == method)
    ].iloc[0]
    return build_bassii_source_claim(
        cells, evidence_cell_id=selected["evidence_cell_id"],
        asserted_value_raw=value, asserted_unit=unit,
    )


def _entry(cells, **kwargs):
    claim = _claim(cells, **kwargs)
    result = verify_bassii_claim(RELEASE, claim)
    return make_bassii_entry(
        claim, result, sequence=1, run_id="test-run",
        recorded_at=datetime(2026, 11, 14, 15, tzinfo=timezone.utc),
    )


def test_all_six_cells_build_distinct_source_claims(cells):
    seen = set()
    for _, row in cells.iterrows():
        claim = build_bassii_source_claim(
            cells, evidence_cell_id=row["evidence_cell_id"],
            asserted_value_raw=row["critical_velocity_raw"],
            asserted_unit="mm/s",
        )
        assert claim["claim_class"] == "SOURCE_TRANSCRIPTION"
        assert claim["data_release_id"] == BASS_RELEASE_ID
        assert claim["source_anchor"] == row["source_anchor"]
        assert "original_test_id" not in claim
        assert verify_bassii_claim(RELEASE, claim)["verdict"] == "SUPPORTED"
        seen.add((claim["o2_percent_condition"], claim["method_origin"]))
    assert len(seen) == 6


def test_experiment_requires_published_uncertainty(cells):
    claim = _claim(cells, value="10")
    observed = verify_bassii_claim(RELEASE, claim)
    assert observed["verdict"] == "CONTRADICTED"


def test_ledger_keeps_method_raw_value_and_uncertainty(cells):
    entry = _entry(cells)
    assert entry["method_origin"] == "EXPERIMENTAL"
    assert entry["published_value_raw"] == "10±5"
    assert entry["experimental_uncertainty_raw"] == "±5"
    assert entry["value_kind"] == "REPORTED_FINDING"
    assert entry["original_test_id"] == ""
    assert entry["source_refs"][0].endswith("method_experiment")
    assert entry["counterexamples_checked"] is False
    assert entry["verdict"] == "SUPPORTED"


def test_models_have_missing_not_zero_uncertainty(cells):
    claim = _claim(cells, method="COMPUTATIONAL_MODEL", value="15")
    result = verify_bassii_claim(RELEASE, claim)
    entry = make_bassii_entry(claim, result, sequence=2, run_id="x")
    assert entry["uncertainty_status"] == "NOT_REPORTED"
    assert entry["experimental_uncertainty_raw"] == ""
    assert entry["value_kind"] == "DERIVED"


def test_ledger_can_export_separate_bassii_json(cells):
    entry = _entry(cells)
    payload = json.loads(bassii_ledger_as_json([entry]))
    assert payload["schema"] == SCHEMA
    assert payload["data_release_id"] == BASS_RELEASE_ID
    assert payload["entry_count"] == 1
    assert payload["entries"][0]["check_results"]["value_match"] == "PASS"
    assert payload["entries"][0]["claim_text"] is None
    assert "two Table 2.1 conditions" in payload["scope"]


def test_claim_and_evidence_are_copied(cells):
    claim = _claim(cells)
    result = verify_bassii_claim(RELEASE, claim)
    entry = make_bassii_entry(claim, result, sequence=1, run_id="run")
    claim["asserted_value_raw"] = "bad"
    result["checks"]["value_match"] = "FAIL"
    assert entry["claim"]["asserted_value_raw"] == "10±5"
    assert entry["check_results"]["value_match"] == "PASS"
    assert entry["evaluation"]["checks"]["value_match"] == "PASS"


def test_flex_release_cannot_enter_bassii_ledger(cells):
    entry = _entry(cells)
    entry["data_release_id"] = "FLEX-R1-SAMPLE-20261114-v1.0"
    with pytest.raises(ValueError, match="Cannot pool"):
        bassii_ledger_as_json([entry])


def test_invalid_or_unmatched_source_cell_rejected(cells):
    with pytest.raises(ValueError, match="Exactly one"):
        build_bassii_source_claim(
            cells, evidence_cell_id="NASA-FAKE", asserted_value_raw="10±5",
            asserted_unit="mm/s",
        )
    with pytest.raises(ValueError, match="numeric claim"):
        _claim(cells, value=" ")
    with pytest.raises(ValueError, match="only mm/s"):
        _claim(cells, unit="kg")


def test_result_identity_mismatch_is_rejected(cells):
    claim = _claim(cells)
    result = verify_bassii_claim(RELEASE, claim)
    result["data_release_id"] = "other"
    with pytest.raises(ValueError, match="BASS-II D7"):
        make_bassii_entry(claim, result, sequence=1, run_id="x")


def test_bass_verdict_and_error_are_separate(cells):
    claim = _claim(cells)
    result = verify_bassii_claim(RELEASE, claim)
    result["technical_state"] = "ERROR"
    with pytest.raises(ValueError, match="inconsistent"):
        make_bassii_entry(claim, result, sequence=1, run_id="x")
    result["verdict"] = None
    entry = make_bassii_entry(claim, result, sequence=1, run_id="x")
    assert entry["technical_state"] == "ERROR"
    assert entry["verdict"] is None


def test_no_mutation_of_source_dataframe(cells):
    original = cells.copy(deep=True)
    _claim(cells)
    pd.testing.assert_frame_equal(cells, original)


def test_translations_present_in_both_languages():
    for key in (
        "bass_verify_title", "bass_verify_cell", "bass_verify_button",
        "bass_verify_ledger", "bass_verify_download", "bass_verify_error",
    ):
        for lang in ("en", "ru"):
            assert tr(key, lang)
    assert "NOT been executed" not in tr("bass_no_evp", "en")
