"""R5.2: evaluate ten preregistered BASS-II D7 scientific claims.

Expected outcomes are used for scoring AFTER the verifier returns, never as
verifier inputs. The four explicit scope codes are human-curated intake labels;
this runner does not interpret natural language.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from src.bassii_d7_loader import BASS_RELEASE_ID, load_bassii_d7
from src.bassii_evp import verify_bassii_claim

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "data" / "releases" / BASS_RELEASE_ID
PROPOSED_FILE = RELEASE / "BASS_II_R5_D7_proposed_claims_v1.json"

# Explicit intake decisions made from the pre-registered claim meanings.
# They are not derived from case expected verdicts and are not NLP.
_SCOPE_CODES = {
    "B07": "GENERAL_CAUSAL_OXYGEN_EFFECT",
    "B08": "UNIVERSAL_SAFE_FLOW_THRESHOLD",
    "B09": "LUNAR_HABITAT_PREDICTION",
    "B10": "MARS_FIRE_SUPPRESSION_CERTIFICATION",
}


def structured_case(source_case: dict) -> dict:
    """Translate only declared audit parameters into an EVP input."""
    result = {
        "data_release_id": source_case["required_data_release_id"],
        "claim_class": source_case["claim_class"],
        "o2_percent_condition": source_case["o2_percent_condition"],
        "method_origin": source_case["method_origin"],
        "asserted_value_raw": source_case["asserted_value_raw"],
        "asserted_unit": source_case["asserted_unit"],
        "source_anchor": source_case["source_anchor"],
    }
    if result["claim_class"] == "SCIENTIFIC_INTERPRETATION_OR_SCOPE":
        code = _SCOPE_CODES.get(source_case["case_id"])
        if code is None:
            raise ValueError("Unreviewed BASS-II scientific-scope intake")
        result["scope_code"] = code
    return result


def run_benchmark(release_dir: Path = RELEASE) -> dict:
    # This upfront check authenticates the release-provided cases JSON as well
    # as raw, curated and QC sources. It does not modify them.
    load_bassii_d7(release_dir)
    proposed = json.loads(
        (release_dir / PROPOSED_FILE.name).read_text(encoding="utf-8")
    )
    cases = proposed["cases"]
    if proposed.get("dataset") != BASS_RELEASE_ID or len(cases) != 10:
        raise ValueError("Unexpected BASS-II preregistered benchmark version")
    if {case["case_id"] for case in cases} != {f"B{i:02d}" for i in range(1, 11)}:
        raise ValueError("BASS-II benchmark case IDs changed")

    observations = []
    for case in cases:
        assert case["execution_status"] == "PROPOSED_NOT_RUN"
        claim = structured_case(case)
        # Expected outcome and original free text are never verifier inputs.
        observed = verify_bassii_claim(release_dir, claim)
        expected = case["expected_scientific_verdict"]
        passed = (observed["verdict"] == expected and observed["technical_state"] == "OK")
        observations.append({
            "case_id": case["case_id"],
            "category": case["category"],
            "original_claim": case["original_claim"],
            "input": claim,
            "expected_verdict": expected,
            "observed_verdict": observed["verdict"],
            "technical_state": observed["technical_state"],
            "passed": passed,
            "evidence": observed,
        })
    return {
        "benchmark": "BASS-II Table 2.1 NASA-EVP R5.2",
        "data_release_id": BASS_RELEASE_ID,
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "cases_total": len(observations),
        "cases_passed": sum(item["passed"] for item in observations),
        "scope_note": (
            "Structured claims only. Scope codes were manually assigned. "
            "No NLP interpretation, physical validation, or autonomous counterexample search."
        ),
        "observations": observations,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", default="artifacts/r5_bassii_benchmark_v0.1.json"
    )
    args = parser.parse_args()
    try:
        report = run_benchmark()
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        print(f"BASS-II benchmark: ERROR — {exc}")
        return 2
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in report["observations"]:
        verdict = item["observed_verdict"]
        print(f"{item['case_id']} {'PASS' if item['passed'] else 'FAIL'}: {verdict} / {item['technical_state']}")
    print(f"BASS-II benchmark: {report['cases_passed']}/{report['cases_total']} PASS")
    print(f"Observed report: {target}")
    return 0 if report["cases_passed"] == report["cases_total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
