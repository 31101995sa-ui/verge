
"""R4.1 independent checks of a Table IX source-cell claim."""

from pathlib import Path

import pandas as pd
import pytest

from src.evidence_verifier import verify_oxygen_transcription
from src.flex_d7_loader import (
    RELEASE_ID,
    load_flex_d7_release,
)


RELEASE_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)

ANCHOR = (
    "NASA/TP-2015-216046|printed_p20|PDF_p26|"
    "Table_IX|FLEX-002"
)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE_DIR)


def check(
    records,
    value="0.21",
    unit="dimensionless mole fraction",
    **kwargs,
):
    params = {
        "experiment_id": "FLEX-002",
        "asserted_value": value,
        "asserted_unit": unit,
        "source_anchor": ANCHOR,
    }
    params.update(kwargs)

    return verify_oxygen_transcription(records, **params)


def test_correct_normalized_decimal_supported(records):
    answer = check(records)

    assert answer["verdict"] == "SUPPORTED"
    assert answer["technical_state"] == "OK"
    assert answer["source_raw_value"] == ".21"
    assert answer["source_anchor"] == ANCHOR
    assert answer["source_qc_status"] == "VERIFIED"
    assert answer["checks"]["value_match"] == "PASS"


def test_deliberately_wrong_034_contradicted(records):
    answer = check(records, "0.34")

    assert answer["verdict"] == "CONTRADICTED"
    assert answer["checks"]["value_match"] == "FAIL"
    assert answer["source_raw_value"] == ".21"


def test_incompatible_unit_contradicted(records):
    answer = check(records, "0.21", "percent")

    assert answer["verdict"] == "CONTRADICTED"
    assert answer["checks"]["unit_match"] == "FAIL"


def test_wrong_anchor_is_not_contradiction(records):
    answer = check(
        records,
        source_anchor="NASA Table IX",
    )

    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["checks"]["locator_match"] == "FAIL"


def test_unknown_experiment_is_not_automatically_false(records):
    answer = check(
        records,
        experiment_id="FLEX-999",
    )

    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["checks"]["record_exists"] == "UNKNOWN"


def test_wrong_release_is_insufficient(records):
    answer = check(
        records,
        data_release_id="OTHER-RELEASE",
    )

    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"


def test_duplicate_record_is_technical_error(records):
    bad = pd.concat(
        [records, records.iloc[[0]]],
        ignore_index=True,
    )

    answer = check(bad)

    assert answer["verdict"] is None
    assert answer["technical_state"] == "ERROR"


def test_source_unchanged_and_qc_metadata_preserved(records):
    original = records.copy(deep=True)

    answer = check(records)

    pd.testing.assert_frame_equal(records, original)

    row = records.loc[
        records.flex_test_id == "FLEX-002"
    ].iloc[0]

    assert answer["source_qc_flags"] == row["qc_qc_flags"]
    assert (
        answer["source_review_reason"]
        == row["qc_review_reason"]
    )
    assert (
        answer["source_blocked_uses"]
        == row["qc_blocked_uses"]
    )


def test_missing_raw_value_is_not_zero(records):
    modified = records.copy(deep=True)

    modified.loc[
        modified.flex_test_id == "FLEX-002",
        "oxygen_mole_fraction_raw",
    ] = "–"

    answer = check(modified)

    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["source_raw_value"] == "–"
