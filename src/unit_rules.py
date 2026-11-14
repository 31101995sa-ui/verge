
"""R4.3a: limited, deterministic unit equivalence for NASA Table IX cells.

No claim verdict is issued here: the source/locator/QC verifier owns that.
"""

from decimal import Decimal, InvalidOperation

# Exact unit spellings only. Factors convert to the base unit per dimension.
_UNITS = {
    "mm": ("length", Decimal("1")),
    "cm": ("length", Decimal("10")),
    "s": ("time", Decimal("1")),
    "mmHg": ("pressure", Decimal("1")),
    "mm²/s": ("burning_rate", Decimal("1")),
    "dimensionless mole fraction": ("mole_fraction", Decimal("1")),
    "%": ("mole_fraction", Decimal("0.01")),
    "percent": ("mole_fraction", Decimal("0.01")),
}


def compare_source_quantity(
    *,
    source_text: str,
    source_unit: str,
    asserted_text: str,
    asserted_unit: str,
) -> dict:
    """Compare claimed and published numbers without rounding or changing raw text.

    `status` is a technical comparison result, NOT a NASA-EVP verdict.
    Accepted conversions are limited to mm<->cm and mole fraction<->percent.
    """
    result = {
        "status": None,
        "source_text": source_text,
        "source_unit": source_unit,
        "asserted_text": asserted_text,
        "asserted_unit": asserted_unit,
        "asserted_in_source_unit": None,
        "conversion_rule": None,
    }

    if source_text in ("", "–", "-"):
        result["status"] = "MISSING_SOURCE"
        return result

    source_spec = _UNITS.get(source_unit)
    if source_spec is None:
        result["status"] = "SOURCE_ERROR"
        return result

    try:
        source = Decimal(source_text)
        if not source.is_finite():
            raise InvalidOperation
    except (InvalidOperation, TypeError, ValueError):
        result["status"] = "SOURCE_ERROR"
        return result

    claimed_spec = _UNITS.get(asserted_unit)
    if claimed_spec is None:
        result["status"] = "UNSUPPORTED_UNIT"
        return result

    if source_spec[0] != claimed_spec[0]:
        result["status"] = "INCOMPATIBLE_UNIT"
        return result

    try:
        asserted = Decimal(asserted_text)
        if not asserted.is_finite():
            raise InvalidOperation
    except (InvalidOperation, TypeError, ValueError):
        result["status"] = "INVALID_ASSERTION"
        return result

    # All factors are exact powers of ten. No float and no rounding.
    multiplier = claimed_spec[1] / source_spec[1]
    converted = asserted * multiplier
    result["asserted_in_source_unit"] = str(converted)
    result["conversion_rule"] = (
        f"{asserted_unit} -> {source_unit}; multiplier={multiplier}"
    )
    result["status"] = "MATCH" if converted == source else "MISMATCH"
    return result
