"""Phase A: Scientific Mission Control presentation never changes NASA evidence."""

from __future__ import annotations

import ast
from pathlib import Path
from string import Formatter

import pandas as pd

from src.bassii_d7_loader import BASS_RELEASE_ID, load_bassii_d7
from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.i18n import TRANSLATIONS, change_language, display_code, tr
from src.mission_control_ui import NAV_KEYS, navigation_labels, overview_metrics

ROOT = Path(__file__).resolve().parents[1]
FLEX = ROOT / "data" / "releases" / RELEASE_ID
BASS = ROOT / "data" / "releases" / BASS_RELEASE_ID


def test_six_navigation_tabs_are_bilingual_and_stable():
    assert len(NAV_KEYS) == 6
    assert navigation_labels("en") == (
        "Overview", "Explore", "Search", "Verify", "Evidence Ledger",
        "Methods & Limitations",
    )
    assert navigation_labels("ru") == (
        "Обзор", "Исследование", "Поиск", "Проверка",
        "Журнал доказательств", "Методы и ограничения",
    )


def test_mission_translation_keys_complete_and_format_safe():
    fmt = Formatter()
    for key in NAV_KEYS:
        assert key in TRANSLATIONS["en"]
        assert key in TRANSLATIONS["ru"]
    for key in TRANSLATIONS["en"]:
        if not key.startswith("mc_"):
            continue
        en = {name for _, name, _, _ in fmt.parse(tr(key, "en")) if name}
        ru = {name for _, name, _, _ in fmt.parse(tr(key, "ru")) if name}
        assert en == ru, key


def test_flex_summary_preserves_audited_record_counts():
    records = load_flex_d7_release(FLEX)
    before = records.copy(deep=True)
    assert overview_metrics(records) == {"records": 17, "verified": 10, "review": 7}
    pd.testing.assert_frame_equal(records, before)


def test_bassii_remains_six_method_cells_not_six_tests():
    cells = load_bassii_d7(BASS)
    assert len(cells) == 6
    assert set(cells["oxygen_percent_raw"]) == {"16", "21"}
    assert set(cells["method_origin"]) == {
        "EXPERIMENTAL", "COMPUTATIONAL_MODEL", "ANALYTICAL_MODEL"
    }
    assert tr("mc_bass_not_tests", "en").startswith("Six method-specific")


def test_language_switch_does_not_clear_widgets_or_ledgers():
    keys = {
        "r2_selected_id": "FLEX-034",
        "r2_fuels": ["Heptane"],
        "r3_evidence_query": "Methanol",
        "r4_english_claim_text": "NASA Table IX lists an oxygen mole fraction of 0.21 for FLEX-002.",
        "r4_ledger_entries": [{"verdict": "SUPPORTED"}],
        "r5_bassii_ledger_entries": [{"verdict": "CONTRADICTED"}],
        "ui_language": "en",
    }
    before = {k: v for k, v in keys.items() if k != "ui_language"}
    assert change_language(keys, "ru") == "ru"
    assert {k: v for k, v in keys.items() if k != "ui_language"} == before
    assert display_code("REVIEW", "ru").startswith("REVIEW —")
    assert display_code("SUPPORTED", "ru").startswith("SUPPORTED —")


def test_app_uses_tabs_with_original_stateful_widget_keys():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert "main" in funcs and "render_flex_explorer" in funcs
    main = ast.get_source_segment(source, funcs["main"])
    explorer = ast.get_source_segment(source, funcs["render_flex_explorer"])
    assert "st.tabs(" in main
    assert "render_flex_explorer(records, language)" in main
    assert "render_bassii_card(" in main
    assert "render_bassii_verification(" in main
    assert "render_evidence_search(records, language)" in main
    assert "render_ledgers(language)" in main
    for widget in (
        "r2_test_id_query", "r2_fuels", "r2_oxygen", "r2_outcomes",
        "r2_qc", "r2_selected_id",
    ):
        assert f'key="{widget}"' in explorer
    assert 'key="r3_evidence_query"' in source
    assert 'key="ui_language"' in main
    # A no-match FLEX filter must not prevent unrelated BASS-II tabs rendering.
    assert "st.stop()" not in explorer


def test_verification_modes_have_separate_ledger_rendering():
    flex = (ROOT / "src/verification_ui.py").read_text(encoding="utf-8")
    bass = (ROOT / "src/bassii_verification_ui.py").read_text(encoding="utf-8")
    card = (ROOT / "src/bassii_card.py").read_text(encoding="utf-8")
    assert "def render_flex_ledger(" in flex
    assert "if show_ledger:" in flex
    assert "def render_bassii_ledger(" in bass
    assert "if show_ledger:" in bass
    assert "if include_verification:" in card
    assert 'key="r4_download_ledger"' in flex
    assert 'key="r5_bassii_ledger_download"' in bass


def test_theme_is_native_streamlit_without_css_overrides():
    config = (ROOT / ".streamlit/config.toml").read_text(encoding="utf-8")
    assert 'base = "dark"' in config
    assert 'primaryColor = "#65C9DE"' in config
    assert 'backgroundColor = "#101B2B"' in config
    ui = (ROOT / "src/mission_control_ui.py").read_text(encoding="utf-8")
    assert "unsafe_allow_html" not in ui
    assert "<style" not in ui
