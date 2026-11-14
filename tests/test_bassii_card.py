"""R5: isolated, manifest-validated BASS-II Table 2.1 Evidence Card tests."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest

from src.bassii_card import bassii_display_table
from src.bassii_d7_loader import BASS_RELEASE_ID, load_bassii_d7

RELEASE = Path(__file__).resolve().parents[1] / "data" / "releases" / BASS_RELEASE_ID


@pytest.fixture
def evidence():
    return load_bassii_d7(RELEASE)


def test_validated_release_has_six_distinct_method_cells(evidence):
    assert len(evidence) == 6
    assert evidence["evidence_cell_id"].is_unique
    assert evidence.groupby("oxygen_percent_raw")["method_origin"].nunique().to_dict() == {
        "16": 3, "21": 3,
    }
    assert set(evidence["value_kind"]) == {"REPORTED_FINDING", "DERIVED"}


def test_exact_raw_values_from_two_published_rows(evidence):
    values = {
        (row["oxygen_percent_raw"], row["method_origin"]): row["critical_velocity_raw"]
        for _, row in evidence.iterrows()
    }
    assert values == {
        ("21", "EXPERIMENTAL"): "10±5",
        ("21", "COMPUTATIONAL_MODEL"): "15",
        ("21", "ANALYTICAL_MODEL"): "7.5",
        ("16", "EXPERIMENTAL"): "30±5",
        ("16", "COMPUTATIONAL_MODEL"): "35",
        ("16", "ANALYTICAL_MODEL"): "10",
    }
    assert set(evidence["critical_velocity_raw_unit"]) == {"mm/s"}


def test_uncertainty_is_not_silently_assigned_to_models(evidence):
    experiments = evidence.loc[evidence["method_origin"] == "EXPERIMENTAL"]
    models = evidence.loc[evidence["method_origin"] != "EXPERIMENTAL"]
    assert experiments["experimental_uncertainty_raw"].tolist() == ["±5", "±5"]
    assert (models["experimental_uncertainty_raw"] == "").all()
    assert (models["uncertainty_status"] == "NOT_REPORTED").all()


def test_provenance_no_invented_test_ids_and_qc_restrictions(evidence):
    assert (evidence["original_test_id"] == "").all()
    assert (evidence["qc_original_test_linkage"] == "UNRESOLVED").all()
    assert (evidence["transcription_review_status"] == "VERIFIED").all()
    assert (evidence["scientific_fitness_status"] == "CONDITIONAL_GO_ONLY").all()
    assert all(
        value.startswith("NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1|")
        for value in evidence["source_anchor"]
    )
    assert all(
        "UNQUALIFIED_CAUSAL_OXYGEN_EFFECT" in value
        and "FLEX_PHYSICAL_METRIC_POOLING" in value
        for value in evidence["qc_blocked_uses"]
    )
    assert "PROSE_26_AND_40_MM_S_NOT_RESOLVED" in " ".join(
        evidence.loc[evidence["oxygen_percent_raw"] == "16", "quality_flags"]
    )


def test_display_preserves_raw_values_and_bilingual_method_distinction(evidence):
    en = bassii_display_table(evidence, "en")
    ru = bassii_display_table(evidence, "ru")
    assert en.shape == ru.shape == (6, 5)
    assert list(en.iloc[:, 3]) == list(ru.iloc[:, 3]) == [
        "10±5 mm/s", "15 mm/s", "7.5 mm/s",
        "30±5 mm/s", "35 mm/s", "10 mm/s",
    ]
    assert "Эксперимент" in ru.iloc[0, 1]
    assert "Численная модель" in ru.iloc[1, 1]
    assert "Теория" in ru.iloc[2, 1]
    assert list(ru.iloc[[1, 2], 4]) == ["Не сообщена", "Не сообщена"]


def test_presentation_is_non_mutating(evidence):
    snapshot = evidence.copy(deep=True)
    bassii_display_table(evidence, "en")
    bassii_display_table(evidence, "ru")
    pd.testing.assert_frame_equal(evidence, snapshot)


def test_manifest_rejects_changed_scientific_csv(tmp_path):
    copy = tmp_path / "release"
    shutil.copytree(RELEASE, copy)
    path = copy / "BASS_II_R5_D7_curated_6cells_v1.csv"
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="hash/size mismatch"):
        load_bassii_d7(copy)


def test_semantic_linkage_rejected_even_when_hash_is_updated(tmp_path):
    copy = tmp_path / "release"
    shutil.copytree(RELEASE, copy)
    name = "BASS_II_R5_D7_QC_6cells_v1.csv"
    path = copy / name
    original = path.read_text(encoding="utf-8-sig")
    assert "UNRESOLVED" in original
    path.write_text(original.replace("UNRESOLVED", "INVENTED", 1), encoding="utf-8-sig")
    manifest_path = copy / "BASS_II_R5_D7_manifest_v1.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload = path.read_bytes()
    manifest["files"][name]["sha256"] = hashlib.sha256(payload).hexdigest()
    manifest["files"][name]["byte_size"] = len(payload)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Inconsistent BASS-II"):
        load_bassii_d7(copy)
