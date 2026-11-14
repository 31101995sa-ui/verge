
"""Deterministic, read-only filters for the bounded FLEX D7 explorer."""

from collections.abc import Sequence

import pandas as pd


REQUIRED_FILTER_COLUMNS = {
    "flex_test_id",
    "fuel_raw",
    "curated_oxygen_mole_fraction",
    "test_end_raw",
    "qc_dap_d4_record_status",
}


def filter_flex_records(
    records: pd.DataFrame,
    *,
    test_id_query: str = "",
    fuels: Sequence[str] = (),
    oxygen_fractions: Sequence[str] = (),
    outcomes: Sequence[str] = (),
    qc_statuses: Sequence[str] = (),
) -> pd.DataFrame:
    """Filter D7 records without changing values, source order or QC fields.

    Oxygen is matched on the D7 normalized text field, so '.21' and
    '0.21' remain distinct in raw data but share the same filter choice.
    """
    missing = REQUIRED_FILTER_COLUMNS - set(records.columns)

    if missing:
        raise ValueError(
            f"Explorer missing required columns: {sorted(missing)}"
        )

    result = records

    # Case-insensitive literal search, not a regular expression.
    query = test_id_query.strip().casefold()

    if query:
        result = result.loc[
            result["flex_test_id"].str.casefold().str.contains(
                query,
                regex=False,
                na=False,
            )
        ]

    # Each active filter narrows the existing result.
    for column, selections in (
        ("fuel_raw", fuels),
        ("curated_oxygen_mole_fraction", oxygen_fractions),
        ("test_end_raw", outcomes),
        ("qc_dap_d4_record_status", qc_statuses),
    ):
        if selections:
            result = result.loc[
                result[column].isin(selections)
            ]

    # Return an independent DataFrame; never mutate D7 records.
    return result.copy()
