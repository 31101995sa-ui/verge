# STELLAR ANVIL — BASS-II R5 / D5 Reconciliation Log v1.0

**DATA_RELEASE_ID (target):** `BASSII-R5-TABLE2_1-20261114-v1.0`  
**Date:** 2026-11-14, Asia/Almaty  
**Source:** NASA/TM-20210011385, Section 2.2 and Table 2.1, printed p. 28 / PDF p. 36  
**D5 verdict:** `PARTIALLY_RECONCILED / NO_SILENT_REPAIR`

## D5-01: Table 2.1 vs experimental prose at nominal 21% O₂

- Table 2.1, printed p.28 / PDF p.36: Experiment `10±5` mm/s.
- Section 2.2.5, printed p.23 / PDF p.31: one gradual-flow test indicates ~`1.1 cm/s` (~11 mm/s); repeated samples of 100, 200, 300 µm about 1 cm/s; 400 µm about 1.5 cm/s.
- Assessment: broad numerical consistency, **not** a proven mathematical reconstruction of the table's `10±5` nor one-to-one identification of any test.
- Status: `CONTEXT_CONSISTENT; TEST_MAPPING_UNRESOLVED`.

## D5-02: Table 2.1 vs experimental prose at nominal 16% O₂

- Table 2.1, printed p.28 / PDF p.36: Experiment `30±5` mm/s.
- Section 2.2.5 continuation, printed p.25 / PDF p.33: approximately `2.6 cm/s` (~26 mm/s) for **100 µm/20 mm width**; approximately `4 cm/s` (~40 mm/s) for **200 µm/10 mm width**.
- The reported ~40 mm/s **does not lie within the simple arithmetic interval 25–35 mm/s**, but the document does not establish that Table 2.1's ±5 is a bound for every individual run. The values may represent different aggregation/conditions; that explanation is a hypothesis, not a verified reconciliation.
- Status: `UNRESOLVED_SUMMARY_TO_PROSE_MAPPING`; preserve the table's `30±5` unchanged, and retain the 26/40 prose values *only as contextual notes*, not additional Table 2.1 evidence cells.

## D5-03: Model provenance, not independent physical experiments

- Table 2.1 includes `Experiment`, `Computation` (Section 2.2.6, printed pp.25–26 / PDF pp.33–34), and `Theory, Equation (2.5)` (printed p.28 / PDF p.36).
- These are three methods producing **six published results under two O₂ conditions**, not six separately observed events.
- Model uncertainty is **not reported**, not zero. Experimental ±5 is not automatically an independent 95% confidence interval.
- Status: `METHOD_ORIGIN_VERIFIED`.

## D5-04: Appendix A.1 test IDs

- Appendix A.1, Table A.1, printed pp.103–104 / PDF pp.111–112, contains Bhattacharjee test matrix with test numbers, sample information, oxygen values, and observation notes.
- Table 2.1 has **no explicit crosswalk** from the six summary cells or two oxygen condition rows to Table A.1's test numbers; conditions in the matrix vary.
- Therefore `original_test_id` remains blank. Do not treat the newly created **audit condition ID** as a NASA as-run test ID.
- Status: `UNRESOLVED_1_TO_1_MAPPING`.

## D5-05: 126/130 project-wide count difference

- Summary/Section 1.1, printed p.3 / PDF p.11 states **126 tests were conducted** (vs 103 planned).
- Prior project audit mentioned **130 PSI records**; this value **has not been independently reproduced or enumerated** in the present targeted audit.
- Categories test / sample / run / PSI repository entry are not interchangeable. Neither count applies to two rows or six evidence cells of Table 2.1.
- Status: `OPEN_SEPARATE_INVESTIGATION / DOES_NOT_BLOCK_BOUNDED_TABLE_RELEASE`.

## Decision / release handling

- GO to D6 for **bounded source-linked transcription and reporting** of Table 2.1.
- NO-GO for unique as-run linkage, inferred statistical significance, isolated causal effect of oxygen, independent physical validation of models, or general spacecraft fire-safety thresholds.
- No original values, uncertainties, or source table rows changed; all unresolved questions are carried forward as QC flags and limitations.
