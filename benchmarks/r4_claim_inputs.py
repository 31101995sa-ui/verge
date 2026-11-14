"""R4.5: transparent manual extraction of asserted quantities from fixture prose.

These are CLAIMED values, not NASA source values or expected verdicts.
The NASA Data Audit fixture remains unchanged. No general NLP is implied.
"""

ASSERTIONS = {
    "T01": ("Methanol", "category"),
    "T02": ("0.21", "dimensionless mole fraction"),
    "T03": ("7.1", "s"),
    "T04": ("0.43", "mm²/s"),
    "T05": ("0.34", "dimensionless mole fraction"),
    "T06": ("1.86", "cm"),
    "T07": (None, None),
    "T08": (None, None),
    "T09": (None, None),
    "T10": (None, None),
    "H01": ("2", "mm"),
    "H02": ("2", "mm"),
    "H03": ("0", "mmHg"),
    "H04": ("0", "mmHg"),
    "H05": ("0", "mm"),
    "H06": ("0", "mm"),
    "H07": ("0", "s"),
    "H08": ("Methanol", "category"),
}


def structured_from_case(case: dict, release_id: str) -> dict:
    """Use fixture identity/locator and independent text-derived assertions."""
    value, unit = ASSERTIONS[case["case_id"]]
    return {
        "data_release_id": release_id,
        "claim_class": case["claim_class"],
        "experiment_id": case["experiment_id"],
        "raw_csv_field": case["raw_csv_field"],
        "asserted_value": value,
        "asserted_unit": unit,
        "source_anchor": case["source_anchor"],
    }
