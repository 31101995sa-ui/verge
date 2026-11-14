
"""Read-only, manifest-checked import of the bounded FLEX R1 D7 release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from src.flex_sample_loader import (
    SAMPLE_COLUMNS,
    QC_COLUMNS,
    _check_keys,
    _read_strings,
)

RELEASE_ID = "FLEX-R1-SAMPLE-20261114-v1.0"
RAW_FILE = "FLEX_R1_D7_raw_17row_v1.csv"
CURATED_FILE = "FLEX_R1_D7_curated_17row_v1.csv"
QC_FILE = "FLEX_R1_D7_QC_17row_v1.csv"

CURATED_REQUIRED = {
    "flex_test_id",
    "source_anchor",
    "quality_status",
    "pressure_field_blocked",
    "extinction_diameter_field_blocked",
    "visible_flame_extinction_droplet_diameter_mm",
}


def load_flex_d7_release(folder: str | Path) -> pd.DataFrame:
    """Return source rows joined one-to-one with curated and QC fields.

    Reject changed files, invalid IDs, unmatched source anchors,
    and inconsistent quality statuses. Do not calculate physical metrics.
    """
    folder = Path(folder)

    manifest = json.loads(
        (folder / "FLEX_R1_D7_manifest_v1.json").read_text(
            encoding="utf-8-sig"
        )
    )

    if manifest.get("data_release_id") != RELEASE_ID:
        raise ValueError("Unexpected FLEX data release ID")

    for name in (RAW_FILE, CURATED_FILE, QC_FILE):
        payload = (folder / name).read_bytes()
        expected = manifest["files"][name]

        if (
            hashlib.sha256(payload).hexdigest() != expected["sha256"]
            or len(payload) != expected["bytes"]
        ):
            raise ValueError(f"Release checksum mismatch: {name}")

    raw = _read_strings(
        folder / RAW_FILE, SAMPLE_COLUMNS, "D7 raw"
    )
    curated = _read_strings(
        folder / CURATED_FILE, CURATED_REQUIRED, "D7 curated"
    )
    qc = _read_strings(
        folder / QC_FILE, QC_COLUMNS, "D7 QC"
    )

    for name, frame in (
        ("D7 raw", raw),
        ("D7 curated", curated),
        ("D7 QC", qc),
    ):
        _check_keys(frame, name)

    ids = set(raw["flex_test_id"])

    for name, frame in (("curated", curated), ("QC", qc)):
        other = set(frame["flex_test_id"])

        if ids != other:
            raise ValueError(
                f"D7 {name} ID mismatch: "
                f"missing={sorted(ids - other)}, "
                f"extra={sorted(other - ids)}"
            )

    curated = curated.rename(
        columns={
            c: f"curated_{c}"
            for c in curated
            if c != "flex_test_id"
        }
    )
    qc = qc.rename(
        columns={
            c: f"qc_{c}"
            for c in qc
            if c != "flex_test_id"
        }
    )

    rows = raw.merge(
        curated,
        on="flex_test_id",
        validate="one_to_one",
        sort=False,
    )

    rows = rows.merge(
        qc,
        on="flex_test_id",
        validate="one_to_one",
        sort=False,
    )

    if not (
        rows["source_anchor"].equals(rows["curated_source_anchor"])
        and rows["source_anchor"].equals(rows["qc_source_anchor"])
    ):
        raise ValueError("D7 source anchor mismatch")

    if not rows["curated_quality_status"].equals(
        rows["qc_dap_d4_record_status"]
    ):
        raise ValueError("D7 QC status mismatch")

    expected_statuses = {"VERIFIED": 10, "REVIEW": 7}

    if (
        len(rows) != 17
        or rows["qc_dap_d4_record_status"].value_counts().to_dict()
        != expected_statuses
    ):
        raise ValueError(
            "Unexpected D7 record count or QC status distribution"
        )

    return rows
