
"""Regression tests for the bounded 17-row FLEX D7 release."""

import hashlib
import json
from pathlib import Path
from shutil import copy2

import pandas as pd
import pytest

from src.flex_d7_loader import (
    CURATED_FILE,
    QC_FILE,
    RAW_FILE,
    load_flex_d7_release,
)

RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data/releases"
    / "FLEX-R1-SAMPLE-20261114-v1.0"
)


def test_d7_17_records_and_field_guards():
    rows = load_flex_d7_release(RELEASE)

    assert len(rows) == 17
    assert rows["flex_test_id"].is_unique

    assert rows["qc_dap_d4_record_status"].value_counts().to_dict() == {
        "VERIFIED": 10,
        "REVIEW": 7,
    }

    by_id = rows.set_index("flex_test_id")

    assert (
        by_id.at[
            "FLEX-034",
            "visible_flame_extinction_diameter_mm_raw",
        ] == "2"
    )
    assert (
        by_id.at[
            "FLEX-034",
            "curated_visible_flame_extinction_droplet_diameter_mm",
        ] == "2"
    )
    assert (
        by_id.at[
            "FLEX-034",
            "curated_extinction_diameter_field_blocked",
        ] == "TRUE"
    )

    assert by_id.at[
        "FLEX-114", "ambient_pressure_mmhg_raw"
    ] == "0"

    assert by_id.at[
        "FLEX-114", "curated_pressure_field_blocked"
    ] == "TRUE"

    assert by_id.at[
        "FLEX-004", "visible_flame_extinction_diameter_mm_raw"
    ] == "–"

    assert by_id.at[
        "FLEX-004",
        "curated_visible_flame_extinction_droplet_diameter_mm",
    ] == ""

    assert by_id.at[
        "FLEX-039", "visible_flame_extinction_diameter_mm_raw"
    ] == "0"

    assert by_id.at[
        "FLEX-039",
        "curated_visible_flame_extinction_droplet_diameter_mm",
    ] == "0"

    assert rows["source_anchor"].equals(
        rows["qc_source_anchor"]
    )
    assert rows["source_anchor"].equals(
        rows["curated_source_anchor"]
    )

    assert rows["qc_blocked_uses"].ne("").all()


def _copy_release(tmp_path):
    for name in (
        RAW_FILE,
        CURATED_FILE,
        QC_FILE,
        "FLEX_R1_D7_manifest_v1.json",
    ):
        copy2(RELEASE / name, tmp_path / name)


def test_d7_changed_csv_rejected(tmp_path):
    _copy_release(tmp_path)

    with (tmp_path / RAW_FILE).open("ab") as stream:
        stream.write(b"\n")

    with pytest.raises(ValueError, match="checksum mismatch"):
        load_flex_d7_release(tmp_path)


def test_d7_unmatched_id_rejected(tmp_path):
    _copy_release(tmp_path)

    file = tmp_path / QC_FILE
    frame = pd.read_csv(
        file,
        dtype=str,
        keep_default_na=False,
        encoding="utf-8-sig",
    )
    frame.loc[0, "flex_test_id"] = "FLEX-999"
    frame.to_csv(file, index=False, encoding="utf-8-sig")

    # Recalculate the temporary test manifest so the ID check
    # is exercised independently from the checksum check.
    manifest_path = tmp_path / "FLEX_R1_D7_manifest_v1.json"
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    payload = file.read_bytes()
    manifest["files"][QC_FILE] = {
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }

    manifest_path.write_text(
        json.dumps(manifest),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="D7 QC ID mismatch"):
        load_flex_d7_release(tmp_path)
