
"""R4.7: narrow English Table IX transcription grammar, not free-form NLP.

Parsing is NOT verification. Only explicitly supported literal Table IX
statements produce a structured claim. The caller must show it for
confirmation and run the manifest-checked NASA-EVP verifier separately.
"""

from __future__ import annotations

import re

import pandas as pd

from src.flex_d7_loader import RELEASE_ID


_NUMBER = r"(?P<value>[+-]?(?:\d+(?:\.\d*)?|\.\d+))"
_TEST = r"(?P<experiment_id>FLEX-\d{3})"

# Each pattern attributes exactly one source cell to NASA Table IX.
# Physical validity, predictions, and causal claims are excluded.
_GRAMMARS = (
    (
        rf"NASA Table IX lists (?P<value>Methanol|Heptane) "
        rf"as the fuel for {_TEST}",
        "fuel_raw",
        "category",
    ),
    (
        rf"NASA Table IX lists an oxygen mole fraction of {_NUMBER}"
        rf"(?: (?P<unit>dimensionless mole fraction|percent|%))?"
        rf" for {_TEST}",
        "oxygen_mole_fraction_raw",
        "dimensionless mole fraction",
    ),
    (
        rf"NASA Table IX lists an initial droplet diameter of "
        rf"{_NUMBER} (?P<unit>mm|cm) for {_TEST}",
        "initial_droplet_diameter_mm_raw",
        "mm",
    ),
    (
        rf"NASA Table IX lists a burn time of {_NUMBER} "
        rf"(?P<unit>s) for {_TEST}",
        "burn_time_s_raw",
        "s",
    ),
    (
        rf"NASA Table IX lists an average burning-rate constant "
        rf"of {_NUMBER} (?P<unit>mm²/s) for {_TEST}",
        "burning_rate_mm2_per_s_raw",
        "mm²/s",
    ),
    (
        rf"NASA Table IX prints {_NUMBER} (?P<unit>mm|cm) "
        rf"as the visible-flame extinction droplet diameter "
        rf"for {_TEST}",
        "visible_flame_extinction_diameter_mm_raw",
        "mm",
    ),
    (
        rf"NASA Table IX prints {_NUMBER} (?P<unit>mmHg) "
        rf"for the ambient pressure of {_TEST}",
        "ambient_pressure_mmhg_raw",
        "mmHg",
    ),
    (
        rf"NASA Table IX reports an extinction droplet diameter "
        rf"of {_NUMBER} (?P<unit>mm|cm) for {_TEST}",
        "visible_flame_extinction_diameter_mm_raw",
        "mm",
    ),
)

_COMPILED = tuple(
    (
        re.compile(
            pattern + r"\.?",
            re.IGNORECASE | re.ASCII,
        ),
        field,
        unit,
    )
    for pattern, field, unit in _GRAMMARS
)


def parse_table_ix_claim(
    text: str,
    records: pd.DataFrame,
) -> dict:
    """Create a candidate claim, never a scientific verdict.

    Records provide the candidate source anchor. The independent
    verifier must reload and validate D7 before evaluating it.
    """

    if not isinstance(text, str):
        return {
            "parse_status": "UNSUPPORTED",
            "reason": "Text is required.",
            "claim": None,
        }

    normalized = " ".join(text.strip().split())

    if not normalized or len(normalized) > 500:
        return {
            "parse_status": "UNSUPPORTED",
            "reason": "Provide one short Table IX claim.",
            "claim": None,
        }

    parsed = None

    for regex, field, default_unit in _COMPILED:
        match = regex.fullmatch(normalized)

        if match:
            if parsed is not None:
                return {
                    "parse_status": "UNSUPPORTED",
                    "reason": "Ambiguous matching grammar.",
                    "claim": None,
                }

            parsed = (match, field, default_unit)

    if parsed is None:
        return {
            "parse_status": "UNSUPPORTED",
            "reason": (
                "Only a single explicitly attributed Table IX "
                "source-cell statement is supported; no causal "
                "or physical-validity claims."
            ),
            "claim": None,
        }

    match, field, default_unit = parsed
    experiment_id = match.group("experiment_id").upper()

    required = {"flex_test_id", "source_anchor"}

    if not required.issubset(records.columns):
        return {
            "parse_status": "SOURCE_UNAVAILABLE",
            "reason": "Missing D7 identity/locator fields.",
            "claim": None,
        }

    selection = records.loc[
        records["flex_test_id"] == experiment_id
    ]

    if len(selection) != 1:
        return {
            "parse_status": "SOURCE_UNAVAILABLE",
            "reason": (
                "Exactly one D7 record is required "
                "for this experiment ID."
            ),
            "claim": None,
        }

    source_anchor = selection.iloc[0]["source_anchor"]

    if not isinstance(source_anchor, str) or not source_anchor:
        return {
            "parse_status": "SOURCE_UNAVAILABLE",
            "reason": "No source anchor for this record.",
            "claim": None,
        }

    claimed_unit = (
        match.groupdict().get("unit") or default_unit
    )

    if claimed_unit.casefold() == "percent":
        claimed_unit = "percent"

    return {
        "parse_status": "PARSED",
        "reason": (
            "Candidate parsed; not verified. "
            "Confirm fields before evaluation."
        ),
        "claim": {
            "data_release_id": RELEASE_ID,
            "claim_class": "SOURCE_TRANSCRIPTION",
            "experiment_id": experiment_id,
            "raw_csv_field": field,
            "asserted_value": match.group("value"),
            "asserted_unit": claimed_unit,
            "source_anchor": source_anchor,
        },
    }
