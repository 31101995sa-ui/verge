"""Standalone R1 D7 release structural tests (Python 3.12+, standard library).

This verifies delivered files/hashes and QC invariants, NOT scientific calibration.
Run in the directory containing this script and the five release artifacts:
    python FLEX_R1_D7_validation_check.py
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from decimal import Decimal

BASE = Path(__file__).resolve().parent
M = json.loads((BASE / "FLEX_R1_D7_manifest_v1.json").read_text(encoding="utf-8"))


def read_csv(filename):
    with (BASE / filename).open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def check_file_hashes():
    for filename, meta in M["files"].items():
        payload = (BASE / filename).read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        assert actual == meta["sha256"], f"Bad SHA-256: {filename}"
        assert len(payload) == meta["bytes"], f"Bad length: {filename}"
    print("PASS: three released CSV files match manifest SHA-256 and byte size")


def check_record_invariants():
    raw = read_csv("FLEX_R1_D7_raw_17row_v1.csv")
    curated = read_csv("FLEX_R1_D7_curated_17row_v1.csv")
    qc = read_csv("FLEX_R1_D7_QC_17row_v1.csv")
    assert len(raw) == len(curated) == len(qc) == 17
    ids = [{r["flex_test_id"] for r in records} for records in (raw, curated, qc)]
    assert len(ids[0]) == 17 and ids[0] == ids[1] == ids[2]
    assert Counter(r["dap_d4_record_status"] for r in qc) == Counter(
        {"VERIFIED": 10, "REVIEW": 7}
    )
    assert Counter(r["quality_status"] for r in curated) == Counter(
        {"VERIFIED": 10, "REVIEW": 7}
    )
    print("PASS: 17 unique source-linked records; 10 VERIFIED / 7 REVIEW")
    return {r["flex_test_id"]: r for r in raw}, {r["flex_test_id"]: r for r in curated}, {r["flex_test_id"]: r for r in qc}


def check_semantics(raw, curated, qc):
    assert raw["FLEX-034"]["visible_flame_extinction_diameter_mm_raw"] == "2"
    assert curated["FLEX-034"]["visible_flame_extinction_droplet_diameter_mm"] == "2"
    assert curated["FLEX-034"]["extinction_diameter_field_blocked"] == "TRUE"
    assert qc["FLEX-034"]["dap_d4_record_status"] == "REVIEW"
    assert "Figure_38" in qc["FLEX-034"]["appendix_b_anchor"]
    assert raw["FLEX-004"]["visible_flame_extinction_diameter_mm_raw"] == "–"
    assert curated["FLEX-004"]["visible_flame_extinction_droplet_diameter_mm"] == ""
    assert raw["FLEX-039"]["visible_flame_extinction_diameter_mm_raw"] == "0"
    assert curated["FLEX-039"]["visible_flame_extinction_droplet_diameter_mm"] == "0"
    assert raw["FLEX-114"]["ambient_pressure_mmhg_raw"] == "0"
    assert curated["FLEX-114"]["pressure_field_blocked"] == "TRUE"
    assert raw["FLEX-009"]["test_time_gmt_raw"] == "–"
    for tid, r in raw.items():
        assert r["source_anchor"] == curated[tid]["source_anchor"] == qc[tid]["source_anchor"]
        assert tid in r["source_anchor"]
        assert "Table_IX" in r["source_anchor"]
        fracs = [Decimal(r[k]) for k in ("oxygen_mole_fraction_raw", "nitrogen_mole_fraction_raw", "carbon_dioxide_mole_fraction_raw", "helium_mole_fraction_raw")]
        assert sum(fracs) == Decimal("1.00"), tid
        if r["test_time_gmt_raw"] != "–":
            datetime.strptime(r["test_date_raw"] + " " + r["test_time_gmt_raw"], "%m/%d/%y %H:%M:%S")
    print("PASS: blocked metrics; literal zero vs em dash; anchors; gas-fraction arithmetic; dates/GMT")


def main():
    assert M["data_release_id"] == "FLEX-R1-SAMPLE-20261114-v1.0"
    check_file_hashes()
    check_semantics(*check_record_invariants())
    print("PASS: FLEX R1 D7 bounded release validation complete")


if __name__ == "__main__":
    main()
