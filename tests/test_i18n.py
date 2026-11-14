"""Dashboard localization: language presentation must not change evidence."""

from __future__ import annotations

import ast
from pathlib import Path
from string import Formatter

import pandas as pd
import pytest

from src.claim_router import verify_claim_from_release
from src.claim_text_parser import parse_table_ix_claim
from src.evidence_ledger import ledger_as_json, make_evidence_entry
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.i18n import (
    CODE_DESCRIPTIONS, FIELD_DESCRIPTIONS, LANGUAGE_KEY,
    LANGUAGES, PARSER_REASONS_RU, QC_FLAGS_RU, SOURCE_NOTE_RU,
    TRANSLATIONS, change_language, display_code, field_label,
    init_language, parser_reason, qc_flags_text, ranking_reason,
    source_note, tr, verifier_summary,
)

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "data" / "releases" / RELEASE_ID


def test_english_default_does_not_clear_existing_state():
    ledger = [{"verdict": "SUPPORTED"}]
    session = {
        "r4_ledger_entries": ledger,
        "r2_fuels": ["Methanol"],
        "r3_evidence_query": "FLEX-002",
        "r2_selected_id": "FLEX-034",
    }
    assert init_language(session) == "en"
    assert session[LANGUAGE_KEY] == "en"
    assert session["r4_ledger_entries"] is ledger
    assert session["r2_selected_id"] == "FLEX-034"


def test_switch_to_russian_and_back_keeps_all_other_state():
    session = {
        LANGUAGE_KEY: "en", "r2_selected_id": "FLEX-034",
        "r2_fuels": ["Methanol"], "r2_qc": ["REVIEW"],
        "r3_evidence_query": "Heptane",
        "r4_ledger_entries": [{"entry_id": "test-1"}],
        "r4_english_claim_text": "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002.",
    }
    original = {k: v for k, v in session.items() if k != LANGUAGE_KEY}
    assert change_language(session, "ru") == "ru"
    assert tr("verification", session[LANGUAGE_KEY]).startswith("Проверка")
    assert {k: v for k, v in session.items() if k != LANGUAGE_KEY} == original
    assert change_language(session, "en") == "en"
    assert {k: v for k, v in session.items() if k != LANGUAGE_KEY} == original


def test_invalid_language_fails_closed():
    with pytest.raises(ValueError):
        change_language({}, "de")
    with pytest.raises(ValueError):
        tr("verification", "de")
    with pytest.raises(KeyError):
        tr("missing_translation", "en")
    assert init_language({LANGUAGE_KEY: "de"}) == "en"


def test_translation_keys_complete_and_placeholders_identical():
    assert set(TRANSLATIONS) == set(LANGUAGES)
    assert set(TRANSLATIONS["en"]) == set(TRANSLATIONS["ru"])
    assert len(TRANSLATIONS["en"]) >= 90
    fmt = Formatter()
    for key in TRANSLATIONS["en"]:
        english = {field for _, field, _, _ in fmt.parse(TRANSLATIONS["en"][key]) if field}
        russian = {field for _, field, _, _ in fmt.parse(TRANSLATIONS["ru"][key]) if field}
        assert english == russian, key
        assert TRANSLATIONS["ru"][key].strip(), key


def test_all_ui_key_calls_have_both_translations():
    used = set()
    for name in ("app.py", "src/verification_ui.py", "src/english_claim_ui.py"):
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        for call in ast.walk(tree):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "tr"
                and call.args
                and isinstance(call.args[0], ast.Constant)
            ):
                used.add(call.args[0].value)
    assert used
    assert used <= set(TRANSLATIONS["en"])


def test_qc_versus_nasa_evp_codes_never_changed():
    for code in ("VERIFIED", "REVIEW", "SUPPORTED", "CONTRADICTED",
                 "INSUFFICIENT_EVIDENCE", "OUT_OF_SCOPE", "ERROR"):
        assert code in CODE_DESCRIPTIONS
        assert display_code(code, "en") == code
        assert display_code(code, "ru").startswith(code + " — ")
    assert "D4" in display_code("VERIFIED", "ru")
    assert "NASA-EVP" in display_code("SUPPORTED", "ru")


def test_source_values_and_units_display_unchanged():
    for value in ("FLEX-034", ".21", "1.86", "0", "–", "mmHg", "mm²/s", "NASA/TP-2015-216046"):
        assert display_code(value, "en") == value
        assert display_code(value, "ru") == value
    assert "FLEX-034" in tr("data_release", "ru", id="FLEX-034")
    assert field_label("oxygen_mole_fraction_raw", "ru") == FIELD_DESCRIPTIONS["oxygen_mole_fraction_raw"]


def test_all_current_qc_notes_are_translated_without_mutating_data():
    records = load_flex_d7_release(RELEASE)
    before = records.copy(deep=True)
    for column in ("qc_review_reason", "qc_blocked_uses", "qc_permitted_uses"):
        for note in set(records[column].tolist()) - {""}:
            assert note in SOURCE_NOTE_RU, (column, note)
            assert source_note(note, "ru") == SOURCE_NOTE_RU[note]
            assert source_note(note, "en") == note
    for flag in set(records["qc_qc_flags"].tolist()):
        assert flag in QC_FLAGS_RU
        assert qc_flags_text(flag, "ru").startswith(flag + " — ")
        assert qc_flags_text(flag, "en") == flag
    pd.testing.assert_frame_equal(records, before)


def test_ranking_explanation_preserves_token_and_weight():
    original = "flex-034: flex_test_id (exact; +100) | review: qc_dap_d4_record_status (exact; +15)"
    localized = ranking_reason(original, "ru")
    assert "flex-034" in localized and "review" in localized
    assert "+100" in localized and "+15" in localized
    assert "точное совпадение" in localized
    assert ranking_reason(original, "en") == original


def test_parser_stays_english_only_in_russian_mode():
    records = load_flex_d7_release(RELEASE)
    english = "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002."
    assert parse_table_ix_claim(english, records)["parse_status"] == "PARSED"
    russian = "В таблице IX NASA мольная доля кислорода 0.21 для FLEX-002."
    result = parse_table_ix_claim(russian, records)
    assert result["parse_status"] == "UNSUPPORTED"
    assert result["claim"] is None
    assert "английские" in tr("english_help", "ru")
    assert parser_reason(result["reason"], "ru") in PARSER_REASONS_RU.values()


def test_verdict_ledger_and_hash_unchanged_by_localization():
    records = load_flex_d7_release(RELEASE)
    row = records.loc[records["flex_test_id"] == "FLEX-002"].iloc[0]
    claim = {
        "data_release_id": RELEASE_ID, "claim_class": "SOURCE_TRANSCRIPTION",
        "experiment_id": "FLEX-002", "raw_csv_field": "oxygen_mole_fraction_raw",
        "asserted_value": "0.21", "asserted_unit": "dimensionless mole fraction",
        "source_anchor": row["source_anchor"],
    }
    result = verify_claim_from_release(RELEASE, claim)
    assert result["verdict"] == "SUPPORTED"
    snapshot = result.copy()
    summary = verifier_summary(result, "ru")
    assert summary and summary != result["explanation"]
    entry = make_evidence_entry(claim, result, sequence=1)
    json_before = ledger_as_json([entry])
    session = {"r4_ledger_entries": [entry], LANGUAGE_KEY: "en"}
    change_language(session, "ru")
    assert ledger_as_json(session["r4_ledger_entries"]) == json_before
    assert result == snapshot


def test_stable_keys_present_for_filters_search_and_verifier():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    verify = (ROOT / "src/verification_ui.py").read_text(encoding="utf-8")
    english = (ROOT / "src/english_claim_ui.py").read_text(encoding="utf-8")
    for key in ("ui_language", "r2_test_id_query", "r2_fuels", "r2_oxygen", "r2_outcomes", "r2_qc", "r2_selected_id", "r3_evidence_query", "r3_selected_evidence_id"):
        assert f'key="{key}"' in app
    for key in ("r4_experiment_id", "r4_claim_class", "r4_raw_field", "r4_asserted_value", "r4_asserted_unit"):
        assert f'key="{key}"' in verify
    assert 'key="r4_english_claim_text"' in english
