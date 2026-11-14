
"""Explainable lexical relevance ranking of source-linked FLEX D7 records.

Scores rank query relevance only; they are not evidence-confidence,
scientific-validity, fire-risk, or physical-performance scores.
"""

from __future__ import annotations

import pandas as pd

from src.flex_d7_loader import RELEASE_ID
from src.retrieval import SEARCH_FIELDS, search_flex_records


# (exact-field match weight, literal substring match weight).
# Source IDs receive priority. QC status is scored only if queried.
FIELD_WEIGHTS = {
    "flex_test_id": (100, 40),
    "fuel_raw": (25, 5),
    "test_end_raw": (25, 5),
    "curated_oxygen_mole_fraction": (20, 4),
    "qc_dap_d4_record_status": (15, 3),
    "qc_qc_flags": (6, 2),
    "qc_review_reason": (3, 1),
    "qc_permitted_uses": (3, 1),
    "qc_blocked_uses": (3, 1),
}

REQUIRED_PROVENANCE = {
    "source_anchor",
    "qc_dap_d4_record_status",
    "qc_blocked_uses",
    "qc_review_reason",
    "curated_pressure_field_blocked",
    "curated_extinction_diameter_field_blocked",
}


def search_and_rank_flex(
    records: pd.DataFrame,
    query: str,
) -> pd.DataFrame:
    """Find D7 records and rank them by explained lexical relevance.

    Preserves every D7 source/QC column.
    Deterministic ties use FLEX ID.
    REVIEW records are not penalized merely for QC status.
    """
    missing = REQUIRED_PROVENANCE - set(records.columns)

    if missing:
        raise ValueError(
            f"Ranking missing provenance fields: {sorted(missing)}"
        )

    if "data_release_id" in records.columns:
        if not records["data_release_id"].eq(RELEASE_ID).all():
            raise ValueError(
                "Ranking received an unexpected data_release_id"
            )

    results = search_flex_records(records, query)

    score_col = "ranking_relevance_score"
    reasons_col = "ranking_reasons"
    position_col = "ranking_position"
    release_col = "data_release_id"

    if results.empty:
        results[score_col] = pd.Series(dtype="int64")
        results[reasons_col] = pd.Series(dtype="object")
        results[position_col] = pd.Series(dtype="int64")
        results[release_col] = pd.Series(dtype="object")
        return results

    tokens = list(dict.fromkeys(query.casefold().split()))

    scores: list[int] = []
    explanations: list[str] = []

    for _, record in results.iterrows():
        total = 0
        matches: list[str] = []

        for token in tokens:
            best_weight = 0
            best_field = ""
            best_kind = ""

            for field in SEARCH_FIELDS:
                value = record[field]

                if not isinstance(value, str):
                    continue

                lowered = value.casefold()
                exact, partial = FIELD_WEIGHTS[field]

                if token == lowered:
                    weight = exact
                elif token in lowered:
                    weight = partial
                else:
                    weight = 0

                if weight > best_weight:
                    best_weight = weight
                    best_field = field
                    best_kind = (
                        "exact" if token == lowered else "substring"
                    )

            if best_weight == 0:
                raise ValueError(
                    f"Retrieval/ranking mismatch for token {token!r}"
                )

            total += best_weight
            matches.append(
                f"{token}: {best_field} "
                f"({best_kind}; +{best_weight})"
            )

        scores.append(total)
        explanations.append(" | ".join(matches))

    results[score_col] = scores
    results[reasons_col] = explanations
    results[release_col] = RELEASE_ID

    results = results.sort_values(
        by=[score_col, "flex_test_id"],
        ascending=[False, True],
        kind="stable",
    ).reset_index(drop=True)

    results[position_col] = range(1, len(results) + 1)

    return results
