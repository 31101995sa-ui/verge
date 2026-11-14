# STELLAR ANVIL — R5 / BASS-II D3–D4 Extraction and Quality Report v0.1

**Date:** 2026-11-14 (Asia/Almaty)  
**State:** D3 complete / D4 completed for Table 2.1 *source transcription and specified methodological provenance*, **not** D5–D7.  
**Source:** *Burning and Suppression of Solids–II (BASS–II) Summary Report*, NASA/TM-20210011385 (October 2021); NTRS `20210011385`; PSI-25.  
**Source PDF:** `TM-20210011385.pdf`, 144 physical pages, SHA-256 `5ffa911fd9b6356f204646003fb9342e341810dcdfdf5cb15756e7f01ec5f770`.  
**Primary locator:** `NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1`.  
**Source:** https://ntrs.nasa.gov/citations/20210011385

## 1. Scope and D3 extraction

Table 2.1 is titled *COMPARISON OF EXTINCTION VELOCITY Vg,cr FOR THIN POLYMETHYLMETHACRYLATE AT 1 atm*. The header supplies **Vg,cr in mm/s**; the row header is **O₂, percent**. A source table row and an experiment are **not equivalent entities**. No unique as-run NASA test IDs are in this table.

| O₂, percent (raw) | Experiment (raw) | Computation (raw) | Theory, Equation (2.5) (raw) | Unit |
|---:|---:|---:|---:|---|
| `21` | `10±5` | `15` | `7.5` | `mm/s` |
| `16` | `30±5` | `35` | `10` | `mm/s` |

**Granularity:** 2 immutable-looking source transcription *rows* in `BASS_II_R5_D3_Table2_1_raw_rows_v0.1.csv` and 6 *method-specific values* in `BASS_II_R5_D3_D4_Table2_1_evidence_cells_v0.1.csv`. These are working D3/D4 artifacts, **not a frozen D7 release**. Internal `audit_row_id`/`audit_condition_id` are explicitly labeled audit keys, not NASA experiment IDs. `original_test_id` remains empty/unknown.

Each evidence cell retains original literal text, raw units, a method, value-kind, explicit `O₂% / 100` normalization, original unit, a source locator down to row/method, PDF SHA-256, quality flags, allowed and blocked uses. The experimental `±5` is stored as both the original notation and a parsed *reported* uncertainty component; its statistical interpretation is **not reported in the table**. For computational/theoretical values, uncertainty is **not reported**, not zero.

**Method semantics:** `Experiment` = `REPORTED_FINDING` from experimental threshold determination; `Computation` = `DERIVED` numerical model output; `Theory` = `DERIVED` analytical model output (Equation 2.5). These are **not six independent physical trials**.

## 2. D4 original-page verification

The original PDF *page 36 (one-based)* was rendered and inspected visually at the table level. Each of the eight raw numerical table entries (2 O₂ conditions + 6 reported method values) was checked against the picture and the corresponding PDF text-word bounding box. All match. The two `±5` symbols were checked directly; `7.5` retains the decimal point. The table's unit `mm/s`, oxygen unit `percent`, caption context `thin polymethylmethacrylate` / `1 atm`, and columns `Experiment`, `Computation`, `Theory, Equation (2.5)` match the source.

| QC check | Result | Specificity |
|---|---|---|
| 6 numeric outputs match Table 2.1 | PASS | Published table transcription only |
| 2 oxygen condition labels match | PASS | Nominal table condition labels |
| Experimental `±5` preserved | PASS | Uncertainty type not inferred |
| Computation vs experiment vs theory classified | PASS | Published method origin preserved |
| Units and explicit oxygen normalization | PASS | `%` is not directly `mole fraction` without division by 100 |
| Original test ID per row | UNKNOWN | Not present in Table 2.1; none created |
| Per-row specimen width/thickness | UNKNOWN | Not assigned in this summary table |
| Independent calibration/physical validity | NOT TESTED | Not established by transcription audit |
| Full report 126 vs PSI 130 reconciliation | OPEN | Separate D5 concern |

**D4 source-transcription status:** `VERIFIED` for six cells as claims about the printed table; **not** `SUPPORTED` scientific interpretations under NASA-EVP. Comparable scientific use remains `CONDITIONAL GO` and may be denied for a particular claim.

## 3. Source context and potential reconciliation questions (D5 input)

**Printed p.23 / PDF p.31, Section 2.2.5:** forced opposed flow is reduced after steady spread; the threshold is a *gas-flow* speed and not the flame spread rate. The authors report about **1.1 cm/s** in one individual low-flow sequence (approximately 11 mm/s after explicit conversion), warn about uncertainty at low-speed fan calibration, boundary layers, and a time lag between adjustments and what the flame experiences.

**Printed p.25 / PDF p.33, Section 2.2.5 continuation:** at lower oxygen the authors describe experimental extinction speeds about **2.6 cm/s** and **4 cm/s** for 100 and 200 μm specimen thickness, respectively; their widths were **20 mm** and **10 mm**. These convert to 26 and 40 mm/s for context. **Neither figure should be silently replaced by the summary `30±5 mm/s`.** The 40 mm/s contextual value is outside a naive [25,35] mm/s interval around the summary central value; this does **not** prove a publication error, because the table's aggregation and ± interpretation are not specified. Flag `AGGREGATION_NOT_RESOLVED` for D5, and **do not use 16% table row as a unique as-run test**.

**Printed p.26 / PDF p.34, Section 2.2.6 and Fig. 2.12:** computational extinction speeds approximately **1.5 and 3.5 cm/s** for 21 and 16% oxygen, respectively; these correspond to Table 2.1's **15 and 35 mm/s**, after explicit `×10` unit conversion. This is a *model result*, not additional experimental validation.

**Printed p.28 / PDF p.36, Sections 2.2.7–2.2.8:** theoretical values derive from Equation (2.5) and assumptions; the authors characterize agreement with experimental and computational results as reasonable in light of experiment uncertainty, simplified mathematics, and scale-analysis error. The article reports an increase in extinction threshold when O₂ is reduced, but this is **a context-bound published interpretation**, not authorization to claim oxygen-only causality for general fuels/spacecraft.

**D5 queue, not completed:** (a) source-summary 16% value vs individual 26/40 mm/s passages; (b) uncertain relation of Table 2.1 rows to actual test-run IDs and differences in width/thickness; (c) whole-report 126 tests vs previously noted 130 PSI entries. These are *open identity and scope issues*, not demonstrated NASA errors.

## 4. QC limitations, allowed/blocked uses

**GO:** literal Table 2.1 source retrieval for both oxygen conditions; separate, source-linked representations of `Experiment` / `Computation` / `Theory` and units.

**CONDITIONAL GO:** source-attributed comparison of reported central estimates for the two O₂ conditions, explicitly labeling differences in methods, uncertain specimen/run mapping, low-velocity instrumentation limitations, and nonexperimental origins of model values. Preserve experimental ±5 exactly without labeling it a standard deviation or CI.

**NO-GO:** treating six values as six independent experiments; inferring a general safe ventilation threshold; describing `Vg,cr` as flame spread rate; pooling BASS-II airflow speed with FLEX droplet size/burn time; per-run causal claims or universal oxygen-only effects; Mars/Moon extrapolation; fire protection certification.

## 5. Reproducible verification receipt

- Original PDF page: physical 36 = `doc[35]` in PyMuPDF; visually inspected.
- Six value pairs in order `(O₂ %, Experiment, Computation, Theory)` were compared against the PDF word bounding boxes, using distinct row and column coordinates.
- CSVs re-opened with UTF-8 BOM-aware reading; counts, uniqueness, values, method semantics, original uncertainty notation, normalization and exact source hash checked.
- Result: **10/10 specified D3/D4 integrity checks PASS**, scoped to transcription, shape and source provenance.
- PDF source SHA-256: `5ffa911fd9b6356f204646003fb9342e341810dcdfdf5cb15756e7f01ec5f770`.
- Raw CSV SHA-256: `4d491ec0d637dde2c848ceede4e1e9c3a674f39f9b0f909ac7ab343c65470be4`.
- Evidence cells CSV SHA-256: `2ade4cbe84d1fe6913bfc339b0a879dc77227d2599c6528ff4136aafad2289e3`.

These checks do not independently reproduce the original experiments, model calculations, or determine physical truth.

## 6. DAP mini-report / next action

**CURRENT GATE:** R5 / D4 complete for six cells of Table 2.1.  
**VERIFIED:** 2 source table rows, 6 published method values, 2 experimental ± components, original title/units/methods and PDF locators.  
**FILES + COMMIT:** two D3/D4 CSVs and this report; local Git untouched/not observed.  
**ISSUES:** as-run ID not in table; p.25 vs Table 2.1 aggregation; low-speed calibration; 126/130 PSI issue; document imagery reuse rights.  
**ONE NEXT ACTION:** targeted **D5**—reconcile the published 16% summary with prose/available test matrices to the degree sources permit.  
**EXIT CRITERION:** a documented explanation *or explicitly unresolved status* for summary-to-run mapping and 16% prose discrepancy; no invented test IDs or changes to raw data.
