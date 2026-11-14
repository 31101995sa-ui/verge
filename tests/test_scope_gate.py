
"""R4.3b tests: scientific limits must never become source-cell support."""

from pathlib import Path

import pandas as pd
import pytest

from src.flex_d7_loader import RELEASE_ID, load_flex_d7_release
from src.scope_gate import evaluate_claim_scope, SCOPE_RULES

RELEASE = (
    Path(__file__).resolve().parents[1]
    / "data" / "releases" / RELEASE_ID
)


@pytest.fixture
def records():
    return load_flex_d7_release(RELEASE)


def check(records, claim_class, experiment_id="FLEX-002", **kwargs):
    anchor = records.set_index("flex_test_id").loc[
        experiment_id, "source_anchor"
    ]
    args = {
        "experiment_id": experiment_id,
        "claim_class": claim_class,
        "source_anchor": anchor,
    }
    args.update(kwargs)
    return evaluate_claim_scope(records, **args)


def test_t07_universal_extinction_causality_is_insufficient(records):
    answer = check(records, "CAUSAL_EFFECT")
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["technical_state"] == "OK"
    assert answer["checks"]["scope_gate"] == "UNKNOWN"
    assert answer["counterexamples_checked"] is False
    assert answer["source_anchor"].endswith("FLEX-002")


def test_t08_universal_oxygen_effect_is_insufficient(records):
    answer = check(records, "CAUSAL_EFFECT", "FLEX-036")
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["printed_page"] == "21"


def test_t09_lunar_extrapolation_out_of_scope(records):
    answer = check(records, "MOON_MARS_EXTRAPOLATION")
    assert answer["verdict"] == "OUT_OF_SCOPE"
    assert answer["checks"]["scope_gate"] == "FAIL"


def test_t10_material_certification_out_of_scope(records):
    answer = check(records, "CERTIFIED_SAFE")
    assert answer["verdict"] == "OUT_OF_SCOPE"


def test_fire_risk_score_out_of_scope(records):
    answer = check(records, "FIRE_RISK_SCORE")
    assert answer["verdict"] == "OUT_OF_SCOPE"


def test_general_threshold_is_insufficient(records):
    answer = check(records, "EXPERIMENTAL_THRESHOLD")
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"


def test_review_record_stays_review(records):
    answer = check(records, "CAUSAL_EFFECT", "FLEX-034")
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["source_qc_status"] == "REVIEW"
    assert answer["source_review_reason"]


def test_no_class_can_issue_supported_or_contradicted(records):
    for kind in SCOPE_RULES:
        answer = check(records, kind)
        assert answer["verdict"] not in {"SUPPORTED", "CONTRADICTED"}


def test_unknown_experiment_is_insufficient(records):
    answer = evaluate_claim_scope(
        records,
        experiment_id="FLEX-999",
        claim_class="CERTIFIED_SAFE",
        source_anchor="invalid",
    )
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["checks"]["record_exists"] == "UNKNOWN"


def test_incorrect_claim_locator_is_insufficient(records):
    answer = check(records, "CERTIFIED_SAFE", source_anchor="wrong")
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["checks"]["locator_match"] == "FAIL"


def test_modified_qc_provenance_is_technical_error(records):
    broken = records.copy(deep=True)
    broken.loc[
        broken.flex_test_id == "FLEX-002", "qc_source_anchor"
    ] = "changed"
    answer = check(broken, "CAUSAL_EFFECT")
    assert answer["verdict"] is None
    assert answer["technical_state"] == "ERROR"


def test_wrong_release_is_insufficient(records):
    answer = check(records, "CAUSAL_EFFECT", data_release_id="UNKNOWN")
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"
    assert answer["checks"]["release_match"] == "FAIL"


def test_original_dataframe_unchanged(records):
    original = records.copy(deep=True)
    check(records, "CAUSAL_EFFECT")
    pd.testing.assert_frame_equal(records, original)


def test_unhandled_claim_class_rejected(records):
    with pytest.raises(ValueError, match="Unsupported scope claim class"):
        check(records, "SOURCE_TRANSCRIPTION")
