
"""R4.3a: exact unit equivalence and integrated Table IX guard tests."""

from pathlib import Path

import pandas as pd
import pytest

from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.field_evidence import verify_table_ix_numeric_claim
from src.unit_rules import compare_source_quantity


RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE)


def check(
    records,
    field,
    value,
    unit,
    test_id="FLEX-002",
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


def test_equivalent_cm_is_supported_with_original_text(records):
    value = check(
        records,
        "initial_droplet_diameter_mm_raw",
        "0.186",
        "cm",
    )

    assert value["verdict"] == "SUPPORTED"
    assert value["source_raw_value"] == "1.86"
    assert value["source_unit"] == "mm"
    assert value["asserted_in_source_unit"] == "1.860"
    assert value["source_anchor"].endswith("FLEX-002")


def test_false_cm_claim_is_contradicted(records):
    value = check(
        records,
        "initial_droplet_diameter_mm_raw",
        "1.86",
        "cm",
    )

    assert value["verdict"] == "CONTRADICTED"
    assert value["checks"]["value_match"] == "FAIL"
    assert value["asserted_in_source_unit"] == "18.60"


def test_same_source_unit_is_supported(records):
    value = check(
        records,
        "initial_droplet_diameter_mm_raw",
        "1.86",
        "mm",
    )

    assert value["verdict"] == "SUPPORTED"
    assert value["technical_state"] == "OK"


def test_incompatible_dimension_contradicted(records):
    value = check(
        records,
        "initial_droplet_diameter_mm_raw",
        "1.86",
        "s",
    )

    assert value["verdict"] == "CONTRADICTED"
    assert value["checks"]["unit_match"] == "FAIL"


def test_unsupported_unit_abstains(records):
    value = check(
        records,
        "initial_droplet_diameter_mm_raw",
        "1.86",
        "furlong",
    )

    assert value["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert value["checks"]["unit_match"] == "UNKNOWN"


def test_blocked_field_stays_blocked_under_conversion(records):
    raw = check(
        records,
        "visible_flame_extinction_diameter_mm_raw",
        "0.2",
        "cm",
        test_id="FLEX-034",
    )

    physical = check(
        records,
        "visible_flame_extinction_diameter_mm_raw",
        "0.2",
        "cm",
        test_id="FLEX-034",
        claim_class="LIMITED_REPORTED_VALUE",
    )

    assert raw["verdict"] == "SUPPORTED"
    assert raw["field_blocked"] is True
    assert physical["verdict"] == "INSUFFICIENT_EVIDENCE"


def test_missing_source_is_not_converted_to_zero(records):
    value = check(
        records,
        "visible_flame_extinction_diameter_mm_raw",
        "0",
        "cm",
        test_id="FLEX-004",
    )

    assert value["source_raw_value"] == "–"
    assert value["verdict"] == "CONTRADICTED"


def test_fraction_equivalent_to_twenty_one_percent():
    result = compare_source_quantity(
        source_text=".21",
        source_unit="dimensionless mole fraction",
        asserted_text="21",
        asserted_unit="%",
    )

    assert result["status"] == "MATCH"
    assert result["asserted_in_source_unit"] == "0.21"


def test_point_two_one_percent_is_not_point_two_one_fraction():
    result = compare_source_quantity(
        source_text=".21",
        source_unit="dimensionless mole fraction",
        asserted_text="0.21",
        asserted_unit="percent",
    )

    assert result["status"] == "MISMATCH"
    assert result["asserted_in_source_unit"] == "0.0021"


def test_nonfinite_is_not_matched():
    result = compare_source_quantity(
        source_text="1.86",
        source_unit="mm",
        asserted_text="NaN",
        asserted_unit="cm",
    )

    assert result["status"] == "INVALID_ASSERTION"


def test_original_dataframe_unmodified(records):
    snapshot = records.copy(deep=True)

    check(
        records,
        "initial_droplet_diameter_mm_raw",
        "0.186",
        "cm",
    )

    pd.testing.assert_frame_equal(records, snapshot)
