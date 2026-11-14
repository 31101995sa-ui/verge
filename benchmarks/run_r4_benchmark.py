"""R4.5: reproducible run of NASA Data Audit's 10+8 predeclared cases.

Only structured claims are verified, not arbitrary English claim text.
No proposed expected verdict is passed to the scientific verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from benchmarks.r4_claim_inputs import ASSERTIONS, structured_from_case
from src.claim_router import verify_claim_from_release
from src.flex_d7_loader import RAW_FILE, CURATED_FILE, QC_FILE, RELEASE_ID

FIXTURE = Path(__file__).with_name("FLEX_R3_R4_Proposed_Claims_v0.1.json")
# Pinned to the unchanged NASA Data Audit handoff bytes.
FROZEN_FIXTURE_SHA256 = "45b26e49a374e666935804a672c6b7e28bf050ac8dad753ecf25b8fd2ef9bff4"
RELEASE = Path(__file__).resolve().parents[1] / "data" / "releases" / RELEASE_ID


def _corrupted_copy(original: Path, target: Path) -> None:
    """Create a TEMPORARY, deliberately corrupted release for H08 only."""
    target.mkdir(parents=True, exist_ok=True)
    for filename in ("FLEX_R1_D7_manifest_v1.json", RAW_FILE, CURATED_FILE, QC_FILE):
        shutil.copy2(original / filename, target / filename)
    with (target / RAW_FILE).open("ab") as stream:
        stream.write(b"\nDELIBERATE_BENCHMARK_CORRUPTION\n")


def run_benchmark(release: Path, fixture: Path) -> dict:
    source_bytes = fixture.read_bytes()
    actual_digest = hashlib.sha256(source_bytes).hexdigest()
    if actual_digest != FROZEN_FIXTURE_SHA256:
        raise ValueError("Science benchmark fixture checksum mismatch")
    declared = json.loads(source_bytes.decode("utf-8-sig"))
    cases = declared["cases"]
    case_ids = [case["case_id"] for case in cases]
    if (
        declared["data_release_id"] != RELEASE_ID
        or len(cases) != 18
        or len(set(case_ids)) != 18
        or set(case_ids) != set(ASSERTIONS)
        or set(declared["core_case_ids"]) != {f"T{i:02d}" for i in range(1, 11)}
    ):
        raise ValueError("Unexpected or modified benchmark case manifest")

    results = []
    for case in cases:
        claim = structured_from_case(case, RELEASE_ID)
        if case["case_id"] == "H08":
            # Inject a real D7 checksum failure. No scientific verdict is fabricated.
            with TemporaryDirectory(prefix="stellar_r4_corrupt_") as temp:
                corrupted = Path(temp) / "release"
                _corrupted_copy(release, corrupted)
                actual = verify_claim_from_release(corrupted, claim)
        else:
            actual = verify_claim_from_release(release, claim)

        passed = (
            actual["verdict"] == case["expected_verdict"]
            and actual["technical_state"] == case["technical_state_expected"]
        )
        results.append({
            "case_id": case["case_id"],
            "group": case["group"],
            "claim_text_en": case["claim_text_en"],
            "structured_claim": claim,
            "expected_verdict": case["expected_verdict"],
            "observed_verdict": actual["verdict"],
            "expected_technical_state": case["technical_state_expected"],
            "observed_technical_state": actual["technical_state"],
            "pass": passed,
            "evidence": actual,
        })

    core = [row for row in results if row["case_id"].startswith("T")]
    supplementary = [row for row in results if row["case_id"].startswith("H")]
    return {
        "schema": "stellar-anvil-r4-benchmark-observed-v0.1",
        "data_release_id": RELEASE_ID,
        "fixture_sha256": actual_digest,
        "scope": "structured claims; original English prose not independently verified",
        "manifest_checked_before_each_case": True,
        "original_d7_untouched": True,
        "cases_total": len(results),
        "cases_passed": sum(row["pass"] for row in results),
        "core_passed": sum(row["pass"] for row in core),
        "core_total": len(core),
        "supplementary_passed": sum(row["pass"] for row in supplementary),
        "supplementary_total": len(supplementary),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=RELEASE)
    parser.add_argument("--fixture", type=Path, default=FIXTURE)
    parser.add_argument("--output", type=Path, default=Path("artifacts/r4_benchmark_v0.1.json"))
    args = parser.parse_args()
    report = run_benchmark(args.release, args.fixture)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for row in report["results"]:
        state = "PASS" if row["pass"] else "FAIL"
        print(f"{row['case_id']} {state}: {row['observed_verdict']} / {row['observed_technical_state']}")
    print(f"R4 benchmark: {report['cases_passed']}/{report['cases_total']} PASS")
    print(f"Observed report: {args.output}")
    return 0 if report["cases_passed"] == report["cases_total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
