
"""R4.7: fail-closed parsing, source checks, and rejected assertions."""

from pathlib import Path

import pytest

from src.claim_router import verify_claim_from_release
from src.claim_text_parser import parse_table_ix_claim
from src.flex_d7_loader import (
    RELEASE_ID,
    load_flex_d7_release,
)


RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "releases"
    / RELEASE_ID
)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE)


@pytest.mark.parametrize(
    "sentence, expected",
    [
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 0.21 for FLEX-002.",
            "SUPPORTED",
        ),
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 0.34 for FLEX-002.",
            "CONTRADICTED",
        ),
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 21 % for FLEX-002.",
            "SUPPORTED",
        ),
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 0.21 percent for FLEX-002.",
            "CONTRADICTED",
        ),
        (
            "NASA Table IX lists an initial droplet diameter "
            "of 0.186 cm for FLEX-002.",
            "SUPPORTED",
        ),
        (
            "NASA Table IX lists an initial droplet diameter "
            "of 1.86 cm for FLEX-002.",
            "CONTRADICTED",
        ),
        (
            "NASA Table IX lists Methanol "
            "as the fuel for FLEX-002.",
            "SUPPORTED",
        ),
        (
            "NASA Table IX prints 2 mm as the visible-flame "
            "extinction droplet diameter for FLEX-034.",
            "SUPPORTED",
        ),
        (
            "NASA Table IX prints 0 mmHg for the "
            "ambient pressure of FLEX-114.",
            "SUPPORTED",
        ),
        (
            "NASA Table IX reports an extinction droplet "
            "diameter of 0 mm for FLEX-004.",
            "CONTRADICTED",
        ),
    ],
)
def test_parsed_claim_routes_to_verifier(
    records,
    sentence,
    expected,
):
    proposed = parse_table_ix_claim(sentence, records)

    assert proposed["parse_status"] == "PARSED"
    assert proposed["claim"]["claim_class"] == "SOURCE_TRANSCRIPTION"
    assert "claim_text" not in proposed["claim"]

    result = verify_claim_from_release(
        RELEASE,
        proposed["claim"],
    )

    assert result["technical_state"] == "OK"
    assert result["verdict"] == expected


@pytest.mark.parametrize(
    "sentence",
    [
        (
            "FLEX-034 has a scientifically validated "
            "extinction droplet diameter of 2 mm."
        ),
        "Every droplet in microgravity must extinguish at 0.94 mm.",
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 0.21 for FLEX-002, proving it is safe."
        ),
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 0.21 for FLEX-002 and 0.34 for FLEX-003."
        ),
        (
            "NASA Table IX lists an oxygen mole fraction "
            "of 0.21 for FLEX-002 or FLEX-003."
        ),
        "Predict extinction on the Moon using FLEX-002.",
        "NASA Table IX lists oxygen at 21 for FLEX-002.",
        "",
    ],
)
def test_unsupported_text_is_rejected(records, sentence):
    parsed = parse_table_ix_claim(sentence, records)

    assert parsed["parse_status"] == "UNSUPPORTED"
    assert parsed["claim"] is None


def test_unknown_id_does_not_invent_anchor(records):
    parsed = parse_table_ix_claim(
        "NASA Table IX lists an oxygen mole fraction "
        "of 0.21 for FLEX-999.",
        records,
    )

    assert parsed["parse_status"] == "SOURCE_UNAVAILABLE"
    assert parsed["claim"] is None


def test_parser_does_not_modify_source(records):
    original = records.copy(deep=True)

    parse_table_ix_claim(
        "NASA Table IX lists an initial droplet diameter "
        "of 1.86 mm for FLEX-002.",
        records,
    )

    from pandas.testing import assert_frame_equal
    assert_frame_equal(records, original)
