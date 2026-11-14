
"""Tests for non-destructive filtering of the FLEX D7 sample."""

from pathlib import Path

import pandas as pd
import pytest

from src.explorer_filters import filter_flex_records
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release


RELEASE_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)


@pytest.fixture
def records() -> pd.DataFrame:
    return load_flex_d7_release(RELEASE_DIR)


def test_unfiltered_records_are_unchanged(
    records: pd.DataFrame,
) -> None:
    result = filter_flex_records(records)

    assert result is not records
    pd.testing.assert_frame_equal(result, records)
    assert len(result) == 17


def test_oxygen_filter_groups_equivalent_text_forms(
    records: pd.DataFrame,
) -> None:
    result = filter_flex_records(
        records,
        oxygen_fractions=("0.21",),
    )

    assert len(result) == 11
    assert set(result["oxygen_mole_fraction_raw"]) == {
        ".21",
        "0.21",
    }
    assert set(result["curated_oxygen_mole_fraction"]) == {
        "0.21",
    }


def test_combined_fuel_and_qc_filters(
    records: pd.DataFrame,
) -> None:
    result = filter_flex_records(
        records,
        fuels=("Heptane",),
        qc_statuses=("VERIFIED",),
    )

    assert len(result) == 3
    assert set(result["fuel_raw"]) == {"Heptane"}
    assert set(result["qc_dap_d4_record_status"]) == {
        "VERIFIED",
    }


def test_id_search_retains_blocked_fields(
    records: pd.DataFrame,
) -> None:
    result = filter_flex_records(
        records,
        test_id_query="flex-034",
    )

    assert result["flex_test_id"].tolist() == ["FLEX-034"]

    row = result.iloc[0]

    assert row["visible_flame_extinction_diameter_mm_raw"] == "2"
    assert row["curated_extinction_diameter_field_blocked"] == "TRUE"


def test_raw_zero_and_dash_remain_distinct(
    records: pd.DataFrame,
) -> None:
    missing = filter_flex_records(
        records,
        test_id_query="FLEX-004",
    ).iloc[0]

    zero = filter_flex_records(
        records,
        test_id_query="FLEX-039",
    ).iloc[0]

    assert (
        missing["visible_flame_extinction_diameter_mm_raw"]
        == "–"
    )
    assert (
        missing["curated_visible_flame_extinction_droplet_diameter_mm"]
        == ""
    )
    assert (
        zero["visible_flame_extinction_diameter_mm_raw"]
        == "0"
    )
    assert (
        zero["curated_visible_flame_extinction_droplet_diameter_mm"]
        == "0"
    )


def test_no_matches_keep_schema(
    records: pd.DataFrame,
) -> None:
    result = filter_flex_records(
        records,
        test_id_query="FLEX-999",
    )

    assert result.empty
    assert result.columns.tolist() == records.columns.tolist()


def test_missing_required_column_fails_loudly(
    records: pd.DataFrame,
) -> None:
    incomplete = records.drop(
        columns="curated_oxygen_mole_fraction"
    )

    with pytest.raises(
        ValueError,
        match="curated_oxygen_mole_fraction",
    ):
        filter_flex_records(incomplete)
