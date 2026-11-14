
"""Regression tests for lexical ranking, not NASA-EVP."""

from pathlib import Path

import pandas as pd
import pytest

from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.ranking import search_and_rank_flex


RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)


@pytest.fixture
def records() -> pd.DataFrame:
    return load_flex_d7_release(RELEASE)


def test_exact_id_keeps_source_and_block(records):
    result = search_and_rank_flex(records, "FLEX-034")

    assert result["flex_test_id"].tolist() == ["FLEX-034"]

    row = result.iloc[0]

    assert row["ranking_relevance_score"] == 100
    assert row["ranking_position"] == 1
    assert "flex_test_id (exact; +100)" in row["ranking_reasons"]
    assert row["source_anchor"].endswith("FLEX-034")
    assert row["curated_extinction_diameter_field_blocked"] == "TRUE"
    assert row["qc_dap_d4_record_status"] == "REVIEW"
    assert row["data_release_id"] == RELEASE_ID


def test_compound_query_is_explainable(records):
    result = search_and_rank_flex(
        records,
        "Heptane VERIFIED",
    )

    assert result["flex_test_id"].tolist() == [
        "FLEX-035",
        "FLEX-101",
        "FLEX-280",
    ]

    assert result["ranking_relevance_score"].tolist() == [
        40, 40, 40
    ]

    assert all(
        "fuel_raw (exact; +25)" in reason
        for reason in result["ranking_reasons"]
    )

    assert all(
        "qc_dap_d4_record_status (exact; +15)" in reason
        for reason in result["ranking_reasons"]
    )


def test_review_is_not_filtered_or_penalized(records):
    result = search_and_rank_flex(
        records,
        "ZERO_AMBIENT_PRESSURE_BLOCK",
    )

    assert result["flex_test_id"].tolist() == ["FLEX-114"]

    row = result.iloc[0]

    assert row["curated_pressure_field_blocked"] == "TRUE"
    assert row["qc_dap_d4_record_status"] == "REVIEW"


def test_category_match_outranks_incidental_qc_mention(records):
    result = search_and_rank_flex(records, "Extinction")

    exact_rows = result[
        result["test_end_raw"] == "Extinction"
    ]
    incidental_rows = result[
        result["test_end_raw"] != "Extinction"
    ]

    assert not exact_rows.empty

    if not incidental_rows.empty:
        assert (
            exact_rows["ranking_relevance_score"].min()
            > incidental_rows["ranking_relevance_score"].max()
        )


def test_unmatched_and_blank_queries(records):
    for query in ("", "FLEX-999"):
        result = search_and_rank_flex(records, query)

        assert result.empty

        assert {
            "ranking_relevance_score",
            "ranking_reasons",
            "ranking_position",
            "data_release_id",
        }.issubset(result.columns)


def test_original_data_unchanged(records):
    before = records.copy(deep=True)

    search_and_rank_flex(records, "Methanol")

    pd.testing.assert_frame_equal(before, records)


def test_missing_provenance_rejected(records):
    invalid = records.drop(
        columns=["curated_pressure_field_blocked"]
    )

    with pytest.raises(
        ValueError,
        match="provenance fields",
    ):
        search_and_rank_flex(invalid, "Heptane")


def test_duplicate_ids_rejected(records):
    duplicate = pd.concat(
        [records, records.iloc[[0]]],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="duplicate flex_test_id",
    ):
        search_and_rank_flex(duplicate, "Heptane")
