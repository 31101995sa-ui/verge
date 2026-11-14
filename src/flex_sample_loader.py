
"""Read-only join of audited FLEX Table IX sample with D4 QC decisions."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

SAMPLE_COLUMNS = {
    "flex_test_id",
    "source_anchor",
    "fuel_raw",
    "ambient_pressure_mmhg_raw",
    "visible_flame_extinction_diameter_mm_raw",
    "test_end_raw",
}

QC_COLUMNS = {
    "flex_test_id",
    "source_anchor",
    "dap_d4_record_status",
    "qc_flags",
    "permitted_uses",
    "blocked_uses",
    "review_reason",
}


def _read_strings(path: str | Path, required: set[str], label: str) -> pd.DataFrame:
    """Read every CSV value as text, without interpreting dashes or zeros."""
    frame = pd.read_csv(
        path, dtype=str, keep_default_na=False, encoding="utf-8-sig"
    )
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{label}: missing columns {sorted(missing)}")
    return frame


def _check_keys(frame: pd.DataFrame, label: str) -> None:
    """Reject missing, whitespace-altered, or duplicate experiment IDs."""
    ids = frame["flex_test_id"]
    invalid = ids.eq("") | ids.ne(ids.str.strip())
    if invalid.any():
        raise ValueError(f"{label}: blank or padded flex_test_id")
    duplicates = sorted(ids[ids.duplicated(keep=False)].unique().tolist())
    if duplicates:
        raise ValueError(f"{label}: duplicate flex_test_id {duplicates}")
    if frame["source_anchor"].eq("").any():
        raise ValueError(f"{label}: blank source_anchor")


def load_flex_sample(sample_csv: str | Path, qc_csv: str | Path) -> pd.DataFrame:
    """Join source rows and audited QC text, refusing uncertain ID mappings."""
    sample = _read_strings(sample_csv, SAMPLE_COLUMNS, "FLEX sample")
    qc = _read_strings(qc_csv, QC_COLUMNS, "D4 QC")
    _check_keys(sample, "FLEX sample")
    _check_keys(qc, "D4 QC")

    only_sample = sorted(set(sample["flex_test_id"]) - set(qc["flex_test_id"]))
    only_qc = sorted(set(qc["flex_test_id"]) - set(sample["flex_test_id"]))
    if only_sample or only_qc:
        raise ValueError(
            f"Unmatched IDs: sample_only={only_sample}, qc_only={only_qc}"
        )

    # Preserve original source and D4 fields separately.
    qc = qc.rename(
        columns={"source_anchor": "source_anchor_d4", "qc_flags": "qc_flags_d4"}
    )
    joined = sample.merge(
        qc, on="flex_test_id", how="left",
        validate="one_to_one", sort=False
    )
    mismatched = joined.loc[
        joined["source_anchor"] != joined["source_anchor_d4"], "flex_test_id"
    ].tolist()
    if mismatched:
        raise ValueError(f"Source anchor mismatch for IDs: {mismatched}")
    return joined


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect audited FLEX sample and D4 QC"
    )
    parser.add_argument("sample_csv", type=Path)
    parser.add_argument("qc_csv", type=Path)
    args = parser.parse_args()

    rows = load_flex_sample(args.sample_csv, args.qc_csv)
    print(f"Joined records: {len(rows)}")
    print(f"D4 statuses: {rows['dap_d4_record_status'].value_counts().to_dict()}")
    print(
        rows[["flex_test_id", "dap_d4_record_status", "source_anchor"]]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
