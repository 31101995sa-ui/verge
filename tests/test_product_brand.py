"""Public VERGE product branding must not imply NASA endorsement."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_browser_title_is_verge_only():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'page_title="VERGE"' in app


def test_mission_header_is_verge_only():
    ui = (ROOT / "src/mission_control_ui.py").read_text(encoding="utf-8")
    assert 'st.title("◉ VERGE")' in ui


def test_expansion_and_independence_documented():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Verified Evidence and Risk-Governed Exploration" in readme
    assert "not an official NASA product" in readme


def test_active_product_surfaces_do_not_use_old_branding():
    files = (
        "app.py", "src/mission_control_ui.py", "README.md", "SOURCES.md",
        "docs/PROJECT_STATE.md", "docs/R0_COMPLIANCE.md",
        "docs/AI_DISCLOSURE.md", "docs/DEPLOYMENT.md", "requirements.txt",
    )
    forbidden = ("VERGE-NASA", "VERGE — NASA Edition", "VERGE · NASA EDITION")
    for relative in files:
        value = (ROOT / relative).read_text(encoding="utf-8")
        assert all(name not in value for name in forbidden), relative


def test_nasa_original_source_citations_unchanged():
    sources = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    assert "NASA/TP-2015-216046" in sources
    assert "NASA/TM-20210011385" in sources
