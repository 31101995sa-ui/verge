
"""Regression checks for the deterministic FLEX metadata-search baseline."""

from pathlib import Path

import pandas as pd
import pytest

from src.flex_d7_loader import (
    RELEASE_ID,
    load_flex_d7_release,
)
from src.retrieval import search_flex_records


RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)


@pytest.fixture
def records() -> pd.DataFrame:
    return load_flex_d7_release(RELEASE)


def test_exact_id_returns_anchor_and_review_flag(records):
    found = search_flex_records(records, "FLEX-034")

    assert found["flex_test_id"].tolist() == ["FLEX-034"]

    row = found.iloc[0]

    assert row["qc_dap_d4_record_status"] == "REVIEW"
    assert (
        row["visible_flame_extinction_diameter_mm_raw"]
        == "2"
    )
    assert (
        row["curated_extinction_diameter_field_blocked"]
        == "TRUE"
    )
    assert "FLEX-034" in row["source_anchor"]
    assert "flex_test_id" in row["retrieval_matched_fields"]


def test_query_terms_can_match_across_fields(records):
    found = search_flex_records(
        records,
        "hEpTaNe VERIFIED",
    )

    assert len(found) == 3
    assert set(found["fuel_raw"]) == {"Heptane"}
    assert set(found["qc_dap_d4_record_status"]) == {
        "VERIFIED"
    }

    assert all(
        "fuel_raw" in hits
        and "qc_dap_d4_record_status" in hits
        for hits in found["retrieval_matched_fields"]
    )


def test_conflicting_query_returns_no_rows(records):
    found = search_flex_records(
        records,
        "FLEX-034 Heptane",
    )

    assert found.empty
    assert "retrieval_matched_fields" in found.columns


def test_review_case_retrievable_from_qc_flags(records):
    found = search_flex_records(
        records,
        "ZERO_AMBIENT_PRESSURE_BLOCK",
    )

    assert found["flex_test_id"].tolist() == [
        "FLEX-114"
    ]

    assert (
        found.iloc[0]["ambient_pressure_mmhg_raw"]
        == "0"
    )

    assert (
        "qc_qc_flags"
        in found.iloc[0]["retrieval_matched_fields"]
    )


def test_blank_query_is_empty_not_all_records(records):
    found = search_flex_records(
        records,
        " \t  ",
    )

    assert found.empty
    assert found.columns.tolist() == [
        *records.columns,
        "retrieval_matched_fields",
    ]


def test_regex_chars_are_literal(records):
    found = search_flex_records(
        records,
        r"FLEX-0.*",
    )

    assert found.empty


def test_source_records_not_modified(records):
    before = records.copy(deep=True)

    search_flex_records(
        records,
        "methanol extinction",
    )

    pd.testing.assert_frame_equal(
        records,
        before,
    )


def test_duplicate_id_is_rejected(records):
    duplicate = pd.concat(
        [records, records.iloc[[0]]],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="duplicate flex_test_id",
    ):
        search_flex_records(
            duplicate,
            "methanol",
        )


def test_missing_anchor_is_rejected(records):
    invalid = records.copy()
    invalid.loc[0, "source_anchor"] = ""

    with pytest.raises(
        ValueError,
        match="requires source_anchor",
    ):
        search_flex_records(
            invalid,
            "FLEX-001",
        )
