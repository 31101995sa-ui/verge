"""Read-only, manifest-validated BASS-II Table 2.1 D7 display loader.

This is DATA presentation, not NASA-EVP scientific-claim verification.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

BASS_RELEASE_ID = "BASSII-R5-TABLE2_1-20261114-v1.0"
BASS_REPORT_URL = "https://ntrs.nasa.gov/citations/20210011385"
_PREFIX = "BASS_II_R5_D7_"
_METHOD_FIELDS = {
    "EXPERIMENTAL": "experiment_raw",
    "COMPUTATIONAL_MODEL": "computation_raw",
    "ANALYTICAL_MODEL": "theory_raw",
}
_METHOD_ORDER = tuple(_METHOD_FIELDS)
_REQUIRED_FILES = {
    f"{_PREFIX}raw_2rows_v1.csv",
    f"{_PREFIX}curated_6cells_v1.csv",
    f"{_PREFIX}QC_6cells_v1.csv",
}


def _read_csv(path: Path) -> pd.DataFrame:
    """Force every source cell to string, preserving blanks and raw ± signs."""
    return pd.read_csv(
        path, dtype=str, keep_default_na=False, encoding="utf-8-sig"
    )


def load_bassii_d7(release_dir: str | Path) -> pd.DataFrame:
    """Verify D7 payload and return six joined, source-linked method cells.

    Raises ValueError/OSError on any release integrity or linkage failure.
    Does not change or rewrite release files.
    """
    root = Path(release_dir)
    manifest = json.loads(
        (root / f"{_PREFIX}manifest_v1.json").read_text(encoding="utf-8")
    )
    if manifest.get("data_release_id") != BASS_RELEASE_ID:
        raise ValueError("BASS-II D7 release ID mismatch")

    files = manifest.get("files", {})
    if not _REQUIRED_FILES.issubset(files):
        raise ValueError("BASS-II manifest is missing required CSV files")

    # Check *every* manifest-listed payload file, including QC explanations.
    for name, expected in files.items():
        if Path(name).name != name:
            raise ValueError(f"Invalid manifest path: {name}")
        payload = (root / name).read_bytes()
        if (
            len(payload) != expected["byte_size"]
            or hashlib.sha256(payload).hexdigest() != expected["sha256"]
        ):
            raise ValueError(f"BASS-II D7 hash/size mismatch: {name}")

    raw = _read_csv(root / f"{_PREFIX}raw_2rows_v1.csv")
    cells = _read_csv(root / f"{_PREFIX}curated_6cells_v1.csv")
    qc = _read_csv(root / f"{_PREFIX}QC_6cells_v1.csv")
    if (len(raw), len(cells), len(qc)) != (2, 6, 6):
        raise ValueError("Expected exactly 2 source rows and 6 cells + 6 QC rows")

    required_raw = {
        "audit_row_id", "o2_percent_raw", "source_anchor", "original_test_id",
        "experiment_raw", "computation_raw", "theory_raw", "table_velocity_unit_raw",
    }
    required_cell = {
        "data_release_id", "evidence_cell_id", "audit_condition_id",
        "original_test_id", "oxygen_percent_raw", "method_origin",
        "critical_velocity_raw", "critical_velocity_raw_unit", "source_anchor",
        "experimental_uncertainty_raw", "uncertainty_status", "value_kind",
        "transcription_review_status", "scientific_fitness_status", "quality_flags",
    }
    required_qc = {
        "evidence_cell_id", "source_anchor", "transcription_review_status",
        "scientific_fitness_status", "blocked_uses", "quality_flags",
        "original_test_linkage", "comparison_warning", "allowed_uses",
    }
    if (
        not required_raw.issubset(raw.columns)
        or not required_cell.issubset(cells.columns)
        or not required_qc.issubset(qc.columns)
    ):
        raise ValueError("Missing BASS-II D7 identity, value or QC fields")
    if (
        raw["audit_row_id"].duplicated().any()
        or cells["evidence_cell_id"].duplicated().any()
        or qc["evidence_cell_id"].duplicated().any()
    ):
        raise ValueError("Duplicate BASS-II row or evidence-cell ID")
    if set(raw["o2_percent_raw"]) != {"21", "16"}:
        raise ValueError("Unexpected BASS-II oxygen summary conditions")
    if set(qc["evidence_cell_id"]) != set(cells["evidence_cell_id"]):
        raise ValueError("BASS-II D7 curated/QC cell IDs do not match")

    by_row = raw.set_index("audit_row_id", drop=False)
    by_qc = qc.set_index("evidence_cell_id", drop=False)
    source_root = "NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1"
    for _, cell in cells.iterrows():
        row_id = cell["audit_condition_id"]
        method = cell["method_origin"]
        oxygen = cell["oxygen_percent_raw"]
        if row_id not in by_row.index or method not in _METHOD_FIELDS:
            raise ValueError("BASS-II row or method mapping is unknown")
        original = by_row.loc[row_id]
        check = by_qc.loc[cell["evidence_cell_id"]]
        suffix = {
            "EXPERIMENTAL": "experiment",
            "COMPUTATIONAL_MODEL": "computation",
            "ANALYTICAL_MODEL": "theory",
        }[method]
        locator = f"{source_root}|O2_{oxygen}pct|method_{suffix}"
        if (
            cell["data_release_id"] != BASS_RELEASE_ID
            or original["o2_percent_raw"] != oxygen
            or original["source_anchor"] != f"{source_root}|O2_{oxygen}pct"
            or original[_METHOD_FIELDS[method]] != cell["critical_velocity_raw"]
            or cell["source_anchor"] != locator
            or check["source_anchor"] != locator
            or cell["critical_velocity_raw_unit"] != "mm/s"
            or original["table_velocity_unit_raw"] != "mm/s"
            or cell["original_test_id"] != ""
            or original["original_test_id"] != ""
            or cell["transcription_review_status"] != "VERIFIED"
            or check["transcription_review_status"] != "VERIFIED"
            or cell["scientific_fitness_status"] != "CONDITIONAL_GO_ONLY"
            or check["scientific_fitness_status"] != "CONDITIONAL_GO_ONLY"
            or cell["quality_flags"] != check["quality_flags"]
            or check["original_test_linkage"] != "UNRESOLVED"
            or "UNQUALIFIED_CAUSAL_OXYGEN_EFFECT" not in check["blocked_uses"]
        ):
            raise ValueError(f"Inconsistent BASS-II D7 source/QC: {row_id}/{method}")
        if method == "EXPERIMENTAL":
            if (
                cell["value_kind"] != "REPORTED_FINDING"
                or cell["experimental_uncertainty_raw"] != "±5"
            ):
                raise ValueError("BASS-II experimental uncertainty is incorrect")
        elif (
            cell["value_kind"] != "DERIVED"
            or cell["experimental_uncertainty_raw"] != ""
            or cell["uncertainty_status"] != "NOT_REPORTED"
        ):
            raise ValueError("BASS-II model uncertainty must remain unreported")

    observed = {
        (str(row["oxygen_percent_raw"]), str(row["method_origin"]))
        for _, row in cells.iterrows()
    }
    if observed != {(o, m) for o in ("21", "16") for m in _METHOD_ORDER}:
        raise ValueError("Expected 3 distinct evidence methods per oxygen condition")

    # Preserve every curated field. Prefix QC fields rather than overwriting them.
    qc_display = qc.rename(columns={
        name: f"qc_{name}" for name in qc.columns if name != "evidence_cell_id"
    })
    result = cells.merge(qc_display, on="evidence_cell_id", validate="one_to_one")
    result = result.assign(
        _oxygen_order=result["oxygen_percent_raw"].map({"21": 0, "16": 1}),
        _method_order=result["method_origin"].map({m: i for i, m in enumerate(_METHOD_ORDER)}),
    ).sort_values(["_oxygen_order", "_method_order"])
    return result.drop(columns=["_oxygen_order", "_method_order"]).reset_index(drop=True)
