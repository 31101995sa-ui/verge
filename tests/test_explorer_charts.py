
"""Tests for limited D7 categorical sample counts."""

from pathlib import Path

import pandas as pd
import pytest

from src.explorer_charts import sample_category_counts
from src.explorer_filters import filter_flex_records
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release


RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE)


def _counts(records, field):
    table = sample_category_counts(records, field)

    return dict(
        zip(table["category"], table["sample_records"])
    )


def test_full_sample_fuel_counts(records):
    assert _counts(records, "fuel_raw") == {
        "Heptane": 5,
        "Methanol": 12,
    }


def test_full_sample_outcome_counts(records):
    assert _counts(records, "test_end_raw") == {
        "Completion": 1,
        "Disruption": 3,
        "Extinction": 13,
    }


def test_qc_status_counts_include_review(records):
    assert _counts(
        records,
        "qc_dap_d4_record_status",
    ) == {
        "REVIEW": 7,
        "VERIFIED": 10,
    }


def test_active_filters_change_count_not_original(records):
    baseline = records.copy(deep=True)

    selected = filter_flex_records(
        records,
        fuels=("Heptane",),
        qc_statuses=("VERIFIED",),
    )

    assert _counts(selected, "fuel_raw") == {
        "Heptane": 3,
    }

    assert _counts(
        selected,
        "qc_dap_d4_record_status",
    ) == {
        "VERIFIED": 3,
    }

    pd.testing.assert_frame_equal(records, baseline)


def test_empty_filter_result_has_schema(records):
    selected = filter_flex_records(
        records,
        test_id_query="FLEX-999",
    )

    counts = sample_category_counts(
        selected,
        "fuel_raw",
    )

    assert counts.empty
    assert counts.columns.tolist() == [
        "category",
        "sample_records",
    ]


def test_numeric_field_rejected(records):
    with pytest.raises(
        ValueError,
        match="not permitted",
    ):
        sample_category_counts(
            records,
            "ambient_pressure_mmhg_raw",
        )


def test_duplicate_id_rejected(records):
    duplicate = pd.concat(
        [records, records.iloc[[0]]],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="duplicate flex_test_id",
    ):
        sample_category_counts(
            duplicate,
            "fuel_raw",
        )
