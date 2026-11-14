"""UI-only chart regression: readable EN/RU labels and correct count axes."""

from pathlib import Path

import pandas as pd
import pytest

from src.chart_presentation import make_count_chart
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release

RELEASE_DIR = (
    Path(__file__).resolve().parents[1]
    / "data" / "releases" / RELEASE_ID
)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE_DIR)


def test_russian_outcomes_horizontal_and_short(records):
    figure = make_count_chart(records, "test_end_raw", "ru")
    assert figure.data[0].orientation == "h"
    assert set(figure.data[0].y) == {
        "Завершение", "Разрушение капли", "Исчезновение пламени"
    }
    assert sorted(figure.data[0].x) == [1, 3, 13]
    assert figure.layout.xaxis.range[0] == 0
    assert figure.layout.xaxis.range[1] > 13
    assert figure.layout.xaxis.fixedrange is True
    assert figure.layout.yaxis.fixedrange is True


def test_english_outcome_keeps_original_labels(records):
    figure = make_count_chart(records, "test_end_raw", "en")
    assert set(figure.data[0].y) == {"Completion", "Disruption", "Extinction"}
    assert sorted(figure.data[0].x) == [1, 3, 13]


def test_russian_hover_preserves_source_code_and_full_explanation(records):
    figure = make_count_chart(records, "test_end_raw", "ru")
    raw_hover = [str(data[0]) for data in figure.data[0].customdata]
    assert any("Extinction — Исчезновение видимого пламени" in text for text in raw_hover)
    assert any("Disruption — Разрушение капли" in text for text in raw_hover)


def test_qc_counts_start_at_zero_and_keep_codes(records):
    figure = make_count_chart(records, "qc_dap_d4_record_status", "ru")
    assert figure.data[0].orientation == "v"
    assert set(figure.data[0].x) == {"VERIFIED", "REVIEW"}
    assert sorted(figure.data[0].y) == [7, 10]
    assert figure.layout.yaxis.range[0] == 0
    assert figure.layout.yaxis.range[1] > 10
    assert figure.layout.yaxis.fixedrange is True
    assert "D4 QC" in figure.layout.title.text


def test_fuel_counts_are_unmodified(records):
    figure = make_count_chart(records, "fuel_raw", "ru")
    assert figure.data[0].orientation == "v"
    assert set(figure.data[0].x) == {"Methanol", "Heptane"}
    assert sorted(figure.data[0].y) == [5, 12]
    assert figure.layout.yaxis.range[0] == 0


def test_filtered_counts_preserve_zero_based_axis(records):
    selected = records.loc[records["fuel_raw"] == "Heptane"]
    figure = make_count_chart(selected, "fuel_raw", "en")
    assert list(figure.data[0].y) == [5]
    assert figure.layout.yaxis.range[0] == 0
    assert figure.layout.yaxis.range[1] > 5


def test_rendering_does_not_mutate_release_dataframe(records):
    original = records.copy(deep=True)
    for field in ("fuel_raw", "test_end_raw", "qc_dap_d4_record_status"):
        make_count_chart(records, field, "ru")
        make_count_chart(records, field, "en")
    pd.testing.assert_frame_equal(records, original)


def test_unknown_language_or_field_is_rejected(records):
    with pytest.raises(ValueError, match="language"):
        make_count_chart(records, "fuel_raw", "de")
    with pytest.raises(ValueError, match="field"):
        make_count_chart(records, "burn_time_s_raw", "en")
