"""R4.5 scientific expectations are compared AFTER independent execution."""

import json
from pathlib import Path

import pytest

from benchmarks.r4_claim_inputs import ASSERTIONS, structured_from_case
from benchmarks.run_r4_benchmark import FIXTURE, RELEASE, run_benchmark
from src.claim_router import verify_claim_from_release
from src.flex_d7_loader import RELEASE_ID


@pytest.fixture(scope="module")
def fixture_cases():
    return json.loads(FIXTURE.read_text(encoding="utf-8-sig"))


@pytest.fixture(scope="module")
def report():
    return run_benchmark(RELEASE, FIXTURE)


def test_all_18_cases_pass(report):
    assert report["cases_total"] == 18
    assert report["cases_passed"] == 18
    assert report["core_passed"] == 10
    assert report["supplementary_passed"] == 8


def test_no_expected_verdict_leaked_into_claims(report):
    for case in report["results"]:
        claim = case["structured_claim"]
        assert "expected_verdict" not in claim
        assert "source_expected_raw_value" not in claim
        assert "technical_state_expected" not in claim
        assert case["evidence"]["free_text_claim_verified"] is False


def test_h08_is_a_real_loader_failure(report):
    h08 = next(row for row in report["results"] if row["case_id"] == "H08")
    assert h08["observed_verdict"] is None
    assert h08["observed_technical_state"] == "ERROR"
    assert h08["evidence"]["checks"]["source_load"] == "ERROR"
    assert "checksum" in h08["evidence"]["explanation"].lower()


def test_fixture_unchanged_and_structured_text_assertions(fixture_cases):
    assert set(ASSERTIONS) == {case["case_id"] for case in fixture_cases["cases"]}
    for case in fixture_cases["cases"]:
        claim = structured_from_case(case, RELEASE_ID)
        assert claim["experiment_id"] == case["experiment_id"]
        assert claim["raw_csv_field"] == case["raw_csv_field"]
        assert claim["source_anchor"] == case["source_anchor"]
        value = claim["asserted_value"]
        if value is not None and case["case_id"] != "H08":
            assert value in case["claim_text_en"]


def test_negative_source_assertion_not_replaced_by_correct_source_value(fixture_cases):
    cases = {case["case_id"]: case for case in fixture_cases["cases"]}
    for case_id in ("T05", "T06", "H05", "H07"):
        source = cases[case_id]
        actual_claim = structured_from_case(source, RELEASE_ID)
        assert actual_claim["asserted_value"] != source["source_expected_raw_value"] or actual_claim["asserted_unit"] != source["source_unit"]


def test_report_contains_exact_nasa_locators(report):
    for case in report["results"]:
        if case["case_id"] == "H08":
            continue
        evidence = case["evidence"]
        assert evidence["source_anchor"] == case["structured_claim"]["source_anchor"]
        assert evidence["source_qc_status"] in ("VERIFIED", "REVIEW")


def test_unknown_locator_not_bypassed_by_benchmark_fixture(fixture_cases):
    case = next(c for c in fixture_cases["cases"] if c["case_id"] == "T02")
    claim = structured_from_case(case, RELEASE_ID)
    claim["source_anchor"] = "wrong_locator"
    answer = verify_claim_from_release(RELEASE, claim)
    assert answer["verdict"] == "INSUFFICIENT_EVIDENCE"


def test_modified_expected_verdict_fixture_is_rejected(tmp_path):
    altered = tmp_path / "modified.json"
    original = FIXTURE.read_bytes()
    altered.write_bytes(original.replace(b'"expected_verdict": "SUPPORTED"', b'"expected_verdict": "CONTRADICTED"', 1))
    with pytest.raises(ValueError, match="fixture checksum mismatch"):
        run_benchmark(RELEASE, altered)
