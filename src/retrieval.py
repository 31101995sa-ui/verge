
"""Literal, source-linked metadata retrieval for the bounded FLEX D7 release.

This is a deterministic keyword baseline, not document-semantic search.
"""

from __future__ import annotations

import pandas as pd


# Only source/QC metadata are searchable. Physical measurements are not
# converted, compared, scored or treated as independent scientific evidence.
SEARCH_FIELDS = (
    "flex_test_id",
    "fuel_raw",
    "test_end_raw",
    "curated_oxygen_mole_fraction",
    "qc_dap_d4_record_status",
    "qc_qc_flags",
    "qc_review_reason",
    "qc_permitted_uses",
    "qc_blocked_uses",
)

REQUIRED_COLUMNS = set(SEARCH_FIELDS) | {"source_anchor"}


def search_flex_records(
    records: pd.DataFrame,
    query: str,
) -> pd.DataFrame:
    """Find D7 records containing every query token in approved text fields.

    Return original rows in original order plus `retrieval_matched_fields`.
    Tokens are case-insensitive literal substrings (not regex expressions).
    Blank queries return an empty result. REVIEW records are not excluded.
    """
    missing = REQUIRED_COLUMNS - set(records.columns)

    if missing:
        raise ValueError(
            f"Retrieval missing required columns: {sorted(missing)}"
        )

    if (
        records["flex_test_id"].isna().any()
        or records["flex_test_id"].eq("").any()
    ):
        raise ValueError(
            "Retrieval requires nonempty flex_test_id"
        )

    if records["flex_test_id"].duplicated().any():
        raise ValueError(
            "Retrieval contains duplicate flex_test_id"
        )

    if (
        records["source_anchor"].isna().any()
        or records["source_anchor"].eq("").any()
    ):
        raise ValueError(
            "Retrieval requires source_anchor"
        )

    tokens = query.casefold().split()

    if not tokens:
        empty = records.iloc[0:0].copy()
        empty["retrieval_matched_fields"] = pd.Series(
            dtype="object"
        )
        return empty

    positions: list[int] = []
    explanations: list[str] = []

    for position, (_, record) in enumerate(
        records.iterrows()
    ):
        values = {
            field: (
                record[field].casefold()
                if isinstance(record[field], str)
                else ""
            )
            for field in SEARCH_FIELDS
        }

        # All query tokens must match at least one field.
        if not all(
            any(
                token in value
                for value in values.values()
            )
            for token in tokens
        ):
            continue

        positions.append(position)

        matched = [
            field
            for field, value in values.items()
            if any(token in value for token in tokens)
        ]

        explanations.append("; ".join(matched))

    result = records.iloc[positions].copy()
    result["retrieval_matched_fields"] = explanations

    return result
