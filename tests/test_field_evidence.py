
"""R4.2: source transcription and field-specific QC restrictions."""

from pathlib import Path

import pandas as pd
import pytest

from src.field_evidence import verify_table_ix_numeric_claim
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release


RELEASE_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)

EXTINCTION = "visible_flame_extinction_diameter_mm_raw"
PRESSURE = "ambient_pressure_mmhg_raw"
BURN_TIME = "burn_time_s_raw"


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE_DIR)


def check(
    records,
    test_id,
    field,
    value,
    unit,
    claim_class="SOURCE_TRANSCRIPTION",
):
    row = records.set_index("flex_test_id").loc[test_id]

    return verify_table_ix_numeric_claim(
        records,
        experiment_id=test_id,
        raw_field=field,
        asserted_value=value,
        asserted_unit=unit,
        source_anchor=row["source_anchor"],
        claim_class=claim_class,
    )


def test_034_raw_two_is_printed_with_conflict(records):
    result = check(
        records, "FLEX-034", EXTINCTION, "2", "mm"
    )

    assert result["verdict"] == "SUPPORTED"
    assert result["source_raw_value"] == "2"
    assert result["field_blocked"] is True
    assert "Figure 38" in result["explanation"]

    assert result["source_figure_anchor"].endswith(
        "Figure_38|FLEX-034"
    )


def test_034_physically_usable_two_abstains(records):
    result = check(
        records,
        "FLEX-034",
        EXTINCTION,
        "2",
        "mm",
        "LIMITED_REPORTED_VALUE",
    )

    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["checks"]["eligibility"] == "FAIL"


def test_114_raw_zero_supported_but_blocked(records):
    result = check(
        records, "FLEX-114", PRESSURE, "0", "mmHg"
    )

    assert result["verdict"] == "SUPPORTED"
    assert result["source_raw_value"] == "0"
    assert result["field_blocked"] is True
    assert "not" in result["explanation"]


def test_114_physical_zero_abstains(records):
    result = check(
        records,
        "FLEX-114",
        PRESSURE,
        "0",
        "mmHg",
        "LIMITED_REPORTED_VALUE",
    )

    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["technical_state"] == "OK"


def test_004_missing_dash_not_zero(records):
    result = check(
        records, "FLEX-004", EXTINCTION, "0", "mm"
    )

    assert result["source_raw_value"] == "–"
    assert result["verdict"] == "CONTRADICTED"


def test_004_literal_dash_can_be_transcribed(records):
    result = check(
        records, "FLEX-004", EXTINCTION, "–", "mm"
    )

    assert result["verdict"] == "SUPPORTED"
    assert result["checks"]["numeric_value"] == "UNKNOWN"


def test_039_raw_zero_not_physical_diameter(records):
    transcription = check(
        records, "FLEX-039", EXTINCTION, "0", "mm"
    )

    physical_use = check(
        records,
        "FLEX-039",
        EXTINCTION,
        "0",
        "mm",
        "LIMITED_REPORTED_VALUE",
    )

    assert transcription["verdict"] == "SUPPORTED"
    assert physical_use["verdict"] == "INSUFFICIENT_EVIDENCE"


def test_009_missing_burn_time_not_zero(records):
    result = check(
        records, "FLEX-009", BURN_TIME, "0", "s"
    )

    assert result["source_raw_value"] == "–"
    assert result["verdict"] == "CONTRADICTED"


def test_wrong_claim_locator_not_supported(records):
    result = verify_table_ix_numeric_claim(
        records,
        experiment_id="FLEX-034",
        raw_field=EXTINCTION,
        asserted_value="2",
        asserted_unit="mm",
        source_anchor="NASA Table IX",
        claim_class="SOURCE_TRANSCRIPTION",
    )

    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert result["checks"]["claim_locator"] == "FAIL"


def test_wrong_unit_rejected(records):
    result = check(
        records, "FLEX-034", EXTINCTION, "2", "mmHg"
    )

    assert result["verdict"] == "CONTRADICTED"


def test_mismatched_internal_provenance_is_error(records):
    bad = records.copy(deep=True)

    bad.loc[
        bad.flex_test_id == "FLEX-034",
        "qc_source_anchor",
    ] = "different"

    result = check(
        bad, "FLEX-034", EXTINCTION, "2", "mm"
    )

    assert result["technical_state"] == "ERROR"
    assert result["verdict"] is None


def test_source_data_remains_unchanged(records):
    original = records.copy(deep=True)

    result = check(
        records, "FLEX-114", PRESSURE, "0", "mmHg"
    )

    pd.testing.assert_frame_equal(records, original)

    assert result["source_qc_status"] == "REVIEW"
    assert (
        "ZERO_AMBIENT_PRESSURE_BLOCK"
        in result["source_qc_flags"]
    )


def test_malformed_source_cell_is_technical_error(records):
    bad = records.copy(deep=True)

    bad.loc[
        bad.flex_test_id == "FLEX-034",
        EXTINCTION,
    ] = "invalid"

    result = check(
        bad, "FLEX-034", EXTINCTION, "2", "mm"
    )

    assert result["technical_state"] == "ERROR"
    assert result["verdict"] is None


def test_malformed_claim_is_not_supported(records):
    result = check(
        records,
        "FLEX-002",
        EXTINCTION,
        "not-a-number",
        "mm",
    )

    assert result["technical_state"] == "OK"
    assert result["verdict"] == "INSUFFICIENT_EVIDENCE"
