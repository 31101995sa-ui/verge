"""R4.6: exportable, session-scoped evidence ledger for structured FLEX claims.

These entries record actual deterministic verifier results, not physical truth.
No files are written automatically; the user must export the ledger.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from collections.abc import Mapping, Sequence

from src.flex_d7_loader import RELEASE_ID

SCHEMA = "stellar-anvil/evidence-ledger-v0.1"
VERDICTS = {
    "SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE", "OUT_OF_SCOPE"
}


def make_evidence_entry(
    claim: Mapping,
    result: Mapping,
    *,
    sequence: int,
    run_id: str = "local-session",
    claim_text: str | None = None,
    recorded_at: datetime | None = None,
) -> dict:
    """Snapshot a claim and its observed verifier result with a traceable ID."""
    if sequence < 1:
        raise ValueError("Ledger sequence must be positive")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("Ledger run_id must be nonempty")
    state = result.get("technical_state")
    verdict = result.get("verdict")
    if state not in {"OK", "ERROR"}:
        raise ValueError("Unknown technical state")
    if (state == "ERROR" and verdict is not None) or (
        state == "OK" and verdict not in VERDICTS
    ):
        raise ValueError("Invalid separation of scientific verdict and technical state")
    if claim.get("data_release_id") != RELEASE_ID:
        raise ValueError("Unexpected claim data release")
    if claim_text is not None and (
        not isinstance(claim_text, str) or not claim_text.strip()
    ):
        raise ValueError("claim_text must be nonempty English text or None")

    moment = recorded_at or datetime.now(timezone.utc)
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("Ledger timestamp must contain a timezone")

    saved_claim = deepcopy(dict(claim))
    saved_result = deepcopy(dict(result))
    # Fingerprint is for local traceability, not a signature or NASA endorsement.
    fingerprint_payload = {
        "sequence": sequence, "claim": saved_claim, "result": saved_result
    }
    if claim_text is not None:
        fingerprint_payload["claim_text"] = claim_text
    fingerprint = sha256(
        json.dumps(
            fingerprint_payload,
            ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:24]

    return {
        "entry_id": fingerprint,
        "run_id": run_id,
        "claim_id": fingerprint,
        "sequence": sequence,
        "timestamp_utc": moment.astimezone(timezone.utc).isoformat(),
        "data_release_id": RELEASE_ID,
        "claim_text": claim_text,  # Original human-confirmed input, when provided.
        "claim": saved_claim,
        "source_refs": [saved_result["source_anchor"]] if saved_result.get("source_anchor") else [],
        "proof_obligation": saved_claim.get("claim_class"),
        "check_results": deepcopy(saved_result.get("checks", {})),
        "counterexamples_checked": bool(saved_result.get("counterexamples_checked", False)),
        "verdict": verdict,
        "technical_state": state,
        "domain_limits": saved_result.get("scope_note") or "17-row FLEX D7 bounded sample only",
        "generation_model_used": None,
        "verifier_version": "R4.4/R4.5 deterministic v0.1",
        "human_review_note": None,
        "evaluation": saved_result,
    }


def ledger_as_json(entries: Sequence[Mapping]) -> str:
    """Export all session entries as readable, UTF-8-safe JSON text."""
    document = {
        "schema": SCHEMA,
        "data_release_id": RELEASE_ID,
        "scope": (
            "Structured Table IX assertions, optionally parsed from a "
            "human-confirmed narrow English grammar; no general free-text "
            "inference, automatic counterexample search, physical safety "
            "assessment, or scientific certification"
        ),
        "entry_count": len(entries),
        "entries": [deepcopy(dict(entry)) for entry in entries],
    }
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"
