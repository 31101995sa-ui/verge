# STELLAR ANVIL — R5 BASS-II Table 2.1 D7 Scientific Release Report v1.0

**DATA_RELEASE_ID:** `BASSII-R5-TABLE2_1-20261114-v1.0`  
**Audit and freeze date:** 2026-11-14 (Asia/Almaty)  
**Release generated:** 2026-11-14T16:41:16+05:00  
**Project:** VERGE-NASA Edition / NASA Space Apps Challenge 2026  
**NASA-DAP status:** D0–D7 completed **only for the bounded Table 2.1**, excluding project-wide experiment reconciliation.  
**Safety:** research/evidence browser release; not certified operational fire safety data.

## 1. Provenance and source identity (D0)

NASA/TP? **No** — source is `NASA/TM-20210011385` (technical memorandum), *Burning and Suppression of Solids–II (BASS–II) Summary Report*, October 2021. Report citation: https://ntrs.nasa.gov/citations/20210011385 . Investigation PSI-25: https://psi.nasa.gov/physci/repo/data/investigations/PSI-25 (DOI 10.60555/4qc4-de67). Local reference PDF `TM-20210011385.pdf`, SHA-256 `5ffa911fd9b6356f204646003fb9342e341810dcdfdf5cb15756e7f01ec5f770`. PSI dataset metadata currently displays CC0-1.0; **do not extrapolate this license to all report figures/PDF**. Original PDF not included in this release ZIP; users must obtain it from NASA. Official 2026 Challenge Resources membership of this exact report remains separately pending.

## 2. Inventory (D1)

- Table 2.1: printed p. 28 / PDF p. 36 (1-based); two oxygen-condition rows, 6 numerical method outputs.
- Experiment source: Section 2.2.5, printed p. 23 / PDF p. 31 and printed p. 25 / PDF p. 33.
- Computational background: Sections 2.2.6–2.2.7, printed pp. 25–28 / PDF pp. 33–36.
- As-run Bhattacharjee matrix: Appendix A.1, printed pp. 103–104 / PDF pp. 111–112; not uniquely mapped to Table 2.1.
- BASS-II report-wide test count (126) is a **different entity** from the 2 table rows / 6 published method results / PSI repository entries.

## 3. Dictionary and extraction (D2–D3)

`BASS_II_R5_D7_raw_2rows_v1.csv` is an exact byte-preserved copy of the earlier D3 Table 2.1 raw-row audit. `BASS_II_R5_D7_curated_6cells_v1.csv` contains the same six source cells with explicit unit, method, oxygen normalization and absence/presence of published uncertainty. Neither acquires artificial experiment IDs.

| O₂ as printed | Experiment (reported, mm/s) | Computation (model, mm/s) | Theory Eq. 2.5 (model, mm/s) |
|---|---:|---:|---:|
| 21% | 10±5 | 15 | 7.5 |
| 16% | 30±5 | 35 | 10 |

Raw source strings are preserved exactly; 21/16 % → 0.21/0.16 are **derived conversions**, not as-run oxygen readings; mm/s remains mm/s. The two ±5 terms are attached to experiment only; four model uncertainties remain `NOT_REPORTED`. The bundled D0–D2 and D3–D4 documents are **historical audit snapshots**: their earlier “D7 not yet executed” status is superseded by this signed-off D7 report and manifest.

## 4. Quality control (D4)

The earlier D4 visual audit compared the two rows and six cells against Table 2.1; the release builder independently checks the source PDF SHA-256, PDF page count, literal table strings, context and D3 values. Six source cells are `VERIFIED` for exact **published source transcription**. The D4 result does **not** mean experimental physics or model predictive validity has been independently confirmed.

## 5. Reconciliation (D5)

See `BASS_II_R5_D7_D5_Reconciliation_Log_v1.md`. Key open issues: (a) 16% O₂ summary `30±5` vs prose approx 26 and 40 mm/s under distinct sample widths/thicknesses, (b) per-run test linkage not established, (c) PSI 130 previous observation vs 126 report tests not re-counted. These are not silently reconciled and do not prevent narrow Table 2.1 source-transcription publication.

## 6. Fitness for use (D6)

See `BASS_II_R5_D7_D6_Fitness_for_Use_v1.md`. **GO** to source lookup and faithful display; **CONDITIONAL GO** to attributed descriptive comparison and method-separated charts with flags; **NO-GO** to general physical causal/predictive/safety claims or cross-class FLEX metric pooling.

## 7. Freeze (D7)

This release consists of exact source rows, curated evidence cells, QC flags, field dictionary, reconciliation log, fitness policy, scientific verification proposals, manifest, and standalone validator. Source document remains externally cited and checksum-identified; D7 CSVs must not be silently edited. To change curated data, create `v1.1` (or newer), regenerate checksums and rerun regression. **Do not overwrite FLEX release.**

## 8. MVP statement and limitations

**2 published Table 2.1 rows / 6 method-specific source cells / 0 uniquely established as-run test IDs from this table.** No claims of comprehensive BASS-II coverage, nor 6 independent measurements. This is a small reproducible source corpus suitable for a BASS-II Evidence Card in a multi-study evidence system.

## 9. Verification result

Build-time checks verify source PDF and exact cells. Independent post-build validator result is saved in `BASS_II_R5_D7_validation_receipt_v1.json` (not a NASA-EVP result). Suggested NASA-EVP claims in `BASS_II_R5_D7_proposed_claims_v1.json` have **NOT BEEN RUN** through the developer verifier.
