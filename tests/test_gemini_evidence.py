"""Offline assertions for both D7 -> Gemini adapters; no API calls."""
from dataclasses import replace
from pathlib import Path

import pytest

from src.bassii_d7_loader import BASS_RELEASE_ID
from src.flex_d7_loader import RELEASE_ID
from src.gemini_candidate import CandidateRejected, generate_candidate
from src.gemini_evidence import build_bassii_snippets, build_flex_snippets
from src.gemini_panel import local_gemini_enabled

ROOT = Path(__file__).resolve().parents[1] / "data" / "releases"


def test_flex_only_verified_d4_and_exact_anchors():
    entries = build_flex_snippets(ROOT / RELEASE_ID)
    assert len(entries) == 10
    ids = {e.evidence_id for e in entries}
    assert {"FLEX-002", "FLEX-003", "FLEX-035"}.issubset(ids)
    assert "FLEX-034" not in ids
    assert "FLEX-114" not in ids
    assert all(e.study == "FLEX" for e in entries)
    assert all(e.source_locator.endswith(e.evidence_id) for e in entries)


def test_flex_preserves_numeric_source_strings_and_restrictions():
    entries = build_flex_snippets(ROOT / RELEASE_ID)
    item = next(x for x in entries if x.evidence_id == "FLEX-002")
    assert "ambient pressure: 762 mmHg" in item.source_text
    assert "droplet diameter at visible flame extinction" in item.source_text
    assert "Blocked uses:" in item.restrictions
    assert "not a scientific verdict" in item.restrictions
    assert all(len(e.source_text) <= 1200 and len(e.restrictions) <= 700 for e in entries)


def test_bassii_all_method_cells_and_original_uncertainty():
    entries = build_bassii_snippets(ROOT / BASS_RELEASE_ID)
    assert len(entries) == 6
    assert len({e.evidence_id for e in entries}) == 6
    assert all(e.study == "BASS-II" for e in entries)
    exp = next(x for x in entries if x.evidence_id == "BASSII_T2_1_O2_21pct|EXPERIMENTAL")
    model = next(x for x in entries if x.evidence_id == "BASSII_T2_1_O2_21pct|COMPUTATIONAL_MODEL")
    assert "10±5 mm/s" in exp.source_text
    assert "NOT_REPORTED" in model.source_text
    assert "not independent experiments" in model.source_text
    assert "No unique as-run test ID mapping" in exp.restrictions
    assert all(len(e.source_text) <= 1200 and len(e.restrictions) <= 700 for e in entries)


def test_manifest_gate_blocks_tampered_flex(tmp_path):
    original = ROOT / RELEASE_ID
    for source in original.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    raw = tmp_path / "FLEX_R1_D7_raw_17row_v1.csv"
    raw.write_bytes(raw.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="checksum"):
        build_flex_snippets(tmp_path)


def test_manifest_gate_blocks_tampered_bassii(tmp_path):
    original = ROOT / BASS_RELEASE_ID
    for source in original.iterdir():
        if source.is_file():
            (tmp_path / source.name).write_bytes(source.read_bytes())
    raw = tmp_path / "BASS_II_R5_D7_raw_2rows_v1.csv"
    raw.write_bytes(raw.read_bytes() + b"tamper")
    with pytest.raises(ValueError, match="hash/size"):
        build_bassii_snippets(tmp_path)


@pytest.mark.parametrize("flag,address,expected", [
    (None, "127.0.0.1", False),
    ("0", "127.0.0.1", False),
    ("1", None, False),
    ("1", "0.0.0.0", False),
    ("1", "localhost", True),
    ("1", "127.0.0.1", True),
])
def test_manual_localhost_gate(flag, address, expected):
    assert local_gemini_enabled(flag, address) is expected


def test_evidence_is_still_subject_to_four_item_contract():
    examples = build_flex_snippets(ROOT / RELEASE_ID)
    with pytest.raises(CandidateRejected, match="one and four"):
        generate_candidate("Explain", examples[:5], client=object())


def test_cross_study_combination_rejected_without_api_call():
    flex = build_flex_snippets(ROOT / RELEASE_ID)[0]
    bass = build_bassii_snippets(ROOT / BASS_RELEASE_ID)[0]
    with pytest.raises(CandidateRejected, match="Cross-study"):
        generate_candidate("Compare", [flex, bass], client=object())
