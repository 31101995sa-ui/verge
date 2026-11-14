"""R5.3: session-scoped, source-linked BASS-II NASA-EVP evidence ledger.

The exported JSON stores observed verifier outputs. The fingerprint is a local
traceability aid, not a signature, certification, or NASA endorsement.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json

from src.bassii_d7_loader import BASS_RELEASE_ID

SCHEMA = "stellar-anvil/bassii-evidence-ledger-v0.1"
_VERDICTS = {
    "SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE", "OUT_OF_SCOPE"
}


def make_bassii_entry(
    claim: Mapping,
    result: Mapping,
    *,
    sequence: int,
    run_id: str,
    recorded_at: datetime | None = None,
) -> dict:
    """Snapshot one BASS-II structured claim and observed evaluation."""
    if not isinstance(sequence, int) or sequence < 1:
        raise ValueError("Sequence must be a positive integer")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("Run ID must be nonempty")
    if (
        claim.get("data_release_id") != BASS_RELEASE_ID
        or result.get("data_release_id") != BASS_RELEASE_ID
    ):
        raise ValueError("Both claim and result must belong to BASS-II D7")
    if claim.get("claim_class") != result.get("claim_class"):
        raise ValueError("Claim class differs from observed evaluation")
    if claim.get("source_anchor") != result.get("asserted_anchor"):
        raise ValueError("Asserted locator differs from evaluated locator")

    state = result.get("technical_state")
    verdict = result.get("verdict")
    if state not in ("OK", "ERROR") or (
        state == "OK" and verdict not in _VERDICTS
    ) or (state == "ERROR" and verdict is not None):
        raise ValueError("Scientific verdict and technical state are inconsistent")

    instant = recorded_at or datetime.now(timezone.utc)
    if instant.tzinfo is None or instant.utcoffset() is None:
        raise ValueError("Timestamp must be timezone-aware")

    saved_claim = deepcopy(dict(claim))
    saved_result = deepcopy(dict(result))
    payload = {"sequence": sequence, "claim": saved_claim, "result": saved_result}
    fingerprint = sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False,
                   separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:24]

    return {
        "entry_id": fingerprint,
        "run_id": run_id,
        "sequence": sequence,
        "timestamp_utc": instant.astimezone(timezone.utc).isoformat(),
        "data_release_id": BASS_RELEASE_ID,
        "claim_text": None,  # No free-text BASS-II claims are parsed or verified.
        "claim": saved_claim,
        "evidence_cell_id": saved_result.get("evidence_cell_id"),
        "source_refs": (
            [saved_result["source_anchor"]]
            if saved_result.get("source_anchor") else []
        ),
        "method_origin": saved_result.get("method_origin"),
        "oxygen_percent_condition": saved_result.get("oxygen_percent_condition"),
        "original_test_id": saved_result.get("original_test_id"),
        "published_value_raw": saved_result.get("source_value_raw"),
        "published_unit": saved_result.get("source_unit"),
        "experimental_uncertainty_raw": saved_result.get("experimental_uncertainty_raw"),
        "uncertainty_status": saved_result.get("uncertainty_status"),
        "value_kind": saved_result.get("value_kind"),
        "qc_blocked_uses": saved_result.get("blocked_uses"),
        "qc_comparison_warning": saved_result.get("comparison_warning"),
        "proof_obligation": saved_claim.get("claim_class"),
        "check_results": deepcopy(saved_result.get("checks", {})),
        "counterexamples_checked": False,
        "verdict": verdict,
        "technical_state": state,
        "domain_limits": saved_result.get("scope_note"),
        "verifier_version": "R5.2 BASS-II deterministic v0.1",
        "generation_model_used": None,
        "evaluation": saved_result,
    }


def bassii_ledger_as_json(entries: Sequence[Mapping]) -> str:
    """Serialize BASS-II session evidence without modifying source D7 files."""
    if any(item.get("data_release_id") != BASS_RELEASE_ID for item in entries):
        raise ValueError("Cannot pool other NASA releases into BASS-II ledger")
    return json.dumps({
        "schema": SCHEMA,
        "data_release_id": BASS_RELEASE_ID,
        "scope": (
            "Six method-specific source cells from two Table 2.1 conditions. "
            "Not six tests; no automatic causal inference, independent "
            "counterexample search, physical prediction, or certification."
        ),
        "entry_count": len(entries),
        "entries": [deepcopy(dict(item)) for item in entries],
    }, indent=2, ensure_ascii=False) + "\n"
