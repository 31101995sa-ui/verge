
"""Descriptive record counts for the bounded FLEX D7 Explorer."""

import pandas as pd


ALLOWED_COUNT_FIELDS = {
    "fuel_raw": "Fuel",
    "test_end_raw": "Reported test end",
    "qc_dap_d4_record_status": "D4 QC status",
}


def sample_category_counts(
    records: pd.DataFrame,
    field: str,
) -> pd.DataFrame:
    """Count audited records by a permitted category.

    This describes the selected sample, not FLEX-wide prevalence.
    Physical measurements are deliberately excluded.
    """

    if field not in ALLOWED_COUNT_FIELDS:
        raise ValueError(
            f"Chart field not permitted: {field}"
        )

    missing = {"flex_test_id", field} - set(records.columns)

    if missing:
        raise ValueError(
            f"Chart source missing columns: {sorted(missing)}"
        )

    if records["flex_test_id"].duplicated().any():
        raise ValueError(
            "Chart source contains duplicate flex_test_id"
        )

    counts = (
        records[field]
        .value_counts(dropna=False, sort=False)
        .rename_axis("category")
        .reset_index(name="sample_records")
        .sort_values("category", kind="stable")
        .reset_index(drop=True)
    )

    return counts
