"""R4.8: confirm narrow English source-cell claims before deterministic verification.

This is a source-claim handoff, NOT general language understanding.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import pandas as pd

from src.claim_router import verify_claim_from_release
from src.claim_text_parser import parse_table_ix_claim


def verify_confirmed_english_claim(
    records: pd.DataFrame,
    release_dir: str | Path,
    *,
    original_text: str,
    candidate: Mapping,
) -> dict:
    """Reparse the exact confirmed text and reject stale/tampered candidates.

    The router subsequently reloads D7 from disk and validates its manifest.
    Do not attach `claim_text` to the router input: it accepts structured
    assertions only. Preserve original text separately in the evidence ledger.
    """
    fresh = parse_table_ix_claim(original_text, records)
    if fresh["parse_status"] != "PARSED" or fresh["claim"] != dict(candidate):
        raise ValueError("Unconfirmed, stale, or modified English claim candidate")
    return verify_claim_from_release(release_dir, fresh["claim"])
