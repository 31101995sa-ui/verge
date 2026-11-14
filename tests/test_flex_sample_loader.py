
"""Regression tests for read-only FLEX sample/QC import."""

from hashlib import sha256
from pathlib import Path

import pandas as pd
import pytest

from src.flex_sample_loader import load_flex_sample

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data/audit/FLEX_TableIX_9row_manual_sample_v0.1.csv"
QC = ROOT / "data/audit/FLEX_D4_9row_QC_status_v0.1.csv"


def _source(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path, dtype=str, keep_default_na=False, encoding="utf-8-sig"
    )


def test_audited_nine_rows_preserve_raw_values() -> None:
    # Audited v0.1 file digests; not a D7 dataset release.
    assert sha256(SAMPLE.read_bytes()).hexdigest() == (
        "ceeec0f8096433c432ea42c89ca7e6e1e530faa16decccff50b8fb7446da4c99"
    )
    assert sha256(QC.read_bytes()).hexdigest() == (
        "991709d37660ad92ef4875645d9e79082f30306fe6fcc2d18211381d09c45cfd"
    )

    source = _source(SAMPLE)
    qc_source = _source(QC)
    joined = load_flex_sample(SAMPLE, QC)

    assert len(joined) == len(source) == len(qc_source) == 9
    pd.testing.assert_frame_equal(joined[source.columns], source)

    assert joined["source_anchor"].equals(joined["source_anchor_d4"])
    assert joined["qc_flags_d4"].equals(qc_source["qc_flags"])
    assert joined["permitted_uses"].equals(qc_source["permitted_uses"])
    assert joined["blocked_uses"].equals(qc_source["blocked_uses"])

    assert joined["dap_d4_record_status"].value_counts().to_dict() == {
        "REVIEW": 6, "VERIFIED": 3
    }

    lookup = joined.set_index("flex_test_id")
    assert lookup.loc["FLEX-002", "oxygen_mole_fraction_raw"] == ".21"
    assert lookup.loc[
        "FLEX-004", "visible_flame_extinction_diameter_mm_raw"
    ] == "–"
    assert lookup.loc["FLEX-009", "test_time_gmt_raw"] == "–"
    assert lookup.loc[
        "FLEX-039", "visible_flame_extinction_diameter_mm_raw"
    ] == "0"
    assert lookup.loc["FLEX-114", "ambient_pressure_mmhg_raw"] == "0"
    assert lookup.loc["FLEX-114", "blocked_uses"] == (
        "Pressure-based calculations; comparisons requiring pressure"
    )


def test_duplicate_id_is_rejected(tmp_path: Path) -> None:
    corrupted = pd.concat(
        [_source(SAMPLE), _source(SAMPLE).iloc[[0]]],
        ignore_index=True
    )
    path = tmp_path / "duplicate.csv"
    corrupted.to_csv(path, index=False, encoding="utf-8-sig")

    with pytest.raises(ValueError, match="duplicate flex_test_id"):
        load_flex_sample(path, QC)


def test_blank_id_is_rejected(tmp_path: Path) -> None:
    altered = _source(SAMPLE)
    altered.loc[0, "flex_test_id"] = ""
    path = tmp_path / "blank_id.csv"
    altered.to_csv(path, index=False, encoding="utf-8-sig")

    with pytest.raises(ValueError, match="blank or padded flex_test_id"):
        load_flex_sample(path, QC)


def test_unmatched_id_is_rejected(tmp_path: Path) -> None:
    altered = _source(QC)
    altered.loc[0, "flex_test_id"] = "FLEX-999"
    path = tmp_path / "unmatched.csv"
    altered.to_csv(path, index=False, encoding="utf-8-sig")

    with pytest.raises(ValueError, match="Unmatched IDs"):
        load_flex_sample(SAMPLE, path)


def test_mismatched_source_anchor_is_rejected(tmp_path: Path) -> None:
    altered = _source(QC)
    altered.loc[0, "source_anchor"] = "wrong-source-anchor"
    path = tmp_path / "wrong_anchor.csv"
    altered.to_csv(path, index=False, encoding="utf-8-sig")

    with pytest.raises(ValueError, match="Source anchor mismatch"):
        load_flex_sample(SAMPLE, path)
