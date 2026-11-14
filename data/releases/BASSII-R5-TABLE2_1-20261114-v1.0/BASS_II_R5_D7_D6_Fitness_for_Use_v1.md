# STELLAR ANVIL — BASS-II R5 / D6 Fitness-for-Use v1.0

**DATA_RELEASE_ID:** `BASSII-R5-TABLE2_1-20261114-v1.0`  
**Scope:** NASA/TM-20210011385 Table 2.1, printed p.28 / PDF p.36 — **2 source rows, 6 method-specific result cells**.

## Scientific scope

Opposed-flow critical **gas** velocity, `V_g,cr`, in ISS microgravity for thermally thin PMMA and 1 atm, comparing nominal 21% O₂ and 16% O₂ across experiment, numerical computation and analytical theory. The critical gas velocity is **not** the flame spread speed `V_f`, and is **not** a generally safe spacecraft ventilation setting.

## Decisions by use case

| Use case | Decision | Guard |
|---|---|---|
| Locate Table 2.1 and display two published O₂ conditions | **GO** | Page/table/method labels and source URL required |
| Exact text/value/uncertainty transcription of a single cell | **GO** | Use original `10±5` or `30±5`, preserve `mm/s`; tag source transcription, not physical validation |
| Show all six values in separate Experimental / Computational / Theoretical rows | **GO** | Method origin and data kind always displayed; no mixing as independent observations |
| Convert percent to fraction or mm/s to cm/s | **CONDITIONAL GO** | Exact Decimal transformation recorded; preserve raw percent and raw mm/s |
| Compare *reported central experimental values* at 21% vs 16% O₂ | **CONDITIONAL GO** | Say “Table 2.1 reports 10±5 and 30±5 mm/s” within this scope; acknowledge differing tested geometries/widths and unknown aggregation; do not claim isolated cause or statistical significance |
| Compare experimental and model values as **published outputs** | **CONDITIONAL GO** | No unreported model confidence intervals; avoid treating models as measured repeats |
| Descriptive grouped plot (O₂ rows × method) | **CONDITIONAL GO** | Explicit title “published critical opposed-flow velocity estimates”; add ±5 only to experimental points, missing uncertainty on models not zero; no trendline |
| Assign source-linked NASA-EVP `SOURCE_TRANSCRIPTION` verdict | **CONDITIONAL GO** | Deterministic verifier checks source/row/method/raw value/unit; DAP VERIFIED is not EVP SUPPORTED by itself |
| Claim exact as-run test IDs and unique sample thickness per row | **NO-GO** | No explicit Table 2.1 ↔ Appendix A.1 mapping |
| Claim all six cells are independent experiments or measurements | **NO-GO** | Mixed experimental and model origins |
| Unqualified causal trend / regression / statistical significance | **NO-GO** | Only two summary oxygen conditions, sample differences and incomplete test linkage |
| General PMMA or spacecraft “safe airflow threshold” | **NO-GO** | Bounded ISS PMMA study, no safety certification |
| Infer Moon/Mars results, suppression settings or apply to FLEX droplet metrics | **NO-GO** | Different gravity regimes and physically incompatible quantities |

## Release-level limitations

1. Values are `REPORTED_FINDING` (experiment) vs `DERIVED` (models); **not** three independent experiments.
2. Two experimental ±5 mm/s components are source-reported and their statistical basis is unspecified in Table 2.1.
3. At lower O₂, Section 2.2.5 discusses ~26 and ~40 mm/s at different PMMA widths and thicknesses; no verified aggregation rule maps them uniquely to 30±5.
4. Low-flow calibration, airflow adjustment lag, tunnel boundary layer are explicitly discussed in Section 2.2.5 (printed p.23 / PDF p.31).
5. Appendix A.1 provides experiment IDs, but no verified 1:1 link to Table 2.1.
6. Pressure 1 atm and oxygen percentages are table context, not six independent sensor readings.

## Recommended Evidence Card language (English)

**Title:** `BASS-II — Opposed-flow radiative extinction (thin PMMA)`  
**Source:** `NASA/TM-20210011385, Table 2.1, printed p. 28 (PDF p. 36)`  
**Caption:** `Published critical opposed-flow gas-velocity results for thin PMMA at 1 atm in ISS microgravity. The two oxygen conditions are summary conditions, and experiment, computation, and theory are distinct evidence methods. Experimental values include reported ±5 mm/s uncertainty; model uncertainties are not specified.`  
**Warning:** `Values describe a restricted experimental and modeling setup. They are not general spacecraft fire-safety limits, and this table alone does not prove an oxygen-only causal effect.`

**Data usage decision:** `GO FOR BOUNDED DISPLAY / CONDITIONAL GO FOR ATTRIBUTED COMPARISON / NO-GO FOR PREDICTION`.
