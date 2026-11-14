# STELLAR ANVIL — BASS-II R5 / NASA-DAP D0–D2 v0.1

**Audit date:** 2026-11-14 (Asia/Almaty)  
**Mode:** NASA-DAP v1.0; M2  
**Status:** D0–D2 completed for **Table 2.1 only**; D3–D7 NOT EXECUTED. This document is a scientific audit note, not a released dataset.

## D0 — Source Card

| Attribute | Evidence / status |
|---|---|
| `source_id` | `NASA_TM_20210011385` |
| Title | *Burning and Suppression of Solids–II (BASS–II) Summary Report* |
| NASA report number | `NASA/TM-20210011385` |
| NTRS citation/document ID | `20210011385`, https://ntrs.nasa.gov/citations/20210011385 |
| Source PDF | `TM-20210011385.pdf`, NASA NTRS download under the citation page |
| Local SHA-256 | `5ffa911fd9b6356f204646003fb9342e341810dcdfdf5cb15756e7f01ec5f770` |
| Local filesize | `48,972,416 bytes` |
| Local page count | `144 physical PDF pages` (PyMuPDF), not to be confused with printed report pagination |
| Publication date | October 2021; NASA NTRS lists October 1, 2021 |
| Document type | NASA Technical Memorandum (TM) |
| Named authors | Sandra L. Olson; Paul V. Ferkul; Subrata Bhattacharjee; Fletcher J. Miller; Carlos Fernandez-Pello; Shmuel Link; James S. T’ien; Indrek Wichman |
| PSI repository | `PSI-25`, https://psi.nasa.gov/physci/repo/data/investigations/PSI-25 |
| PSI DOI | `10.60555/4qc4-de67` |
| PSI version | Version 4, metadata updated 2025-11-24 (current displayed metadata, not the date of the 2021 report) |
| PSI license | `CC0-1.0` for PSI-hosted dataset; **do not automatically apply to the whole technical report or its figures** |
| NTRS public/copyright note | NTRS lists public distribution and the note `Use by or on behalf of the US Gov. Permitted.` This is **not** proof of unrestricted redistribution of every PDF figure |
| Resource provenance | NASA PSI/NTRS confirmed; **official 2026 challenge Resources membership remains to be independently cross-checked** |

**D0 decision:** `IDENTITY VERIFIED / ATTRIBUTION REVIEW`. Source may be studied and cited; publishable reuse of report images and the official Challenge Resources requirement remain open separate checks. Do not claim PSI CC0 covers all PDF contents.

## D1 — Targeted Inventory

**Document focus:** Section **2.2**, “Critical Flow Velocity for Radiative Extinction in Opposed-Flow Flame Spread in Microgravity Environment: Comparison of Experimental, Computational, and Theoretical Results,” printed pp. 19–29; physical PDF pp. 27–37.

| Content | Printed page | Physical PDF page (1-based) | Why relevant |
|---|---:|---:|---|
| Section 2.2.1 abstract and symbol definitions | 19 | 27 | scientific scope, `V_g`, `V_f` |
| Section 2.2.3, Figure 2.6 apparatus schematic | 21 | 29 | sample geometry, airflow, method, microgravity conditions |
| Section 2.2.5 and Figure 2.8 | 23 | 31 | operational extinction threshold; calibration uncertainty |
| Figure 2.9 and Figure 2.10 | 24 | 32 | visual/radiometer support for one test; **not separately quantified measurements for Table 2.1** |
| Section 2.2.5 continuation, 2.2.6 and Figure 2.11 | 25 | 33 | 16% tests, width/thickness caveat; computational method |
| Figure 2.12 and discussion | 26 | 34 | computations at 21% and 16% oxygen |
| Section 2.2.7 and Equations (2.3)–(2.4) | 27 | 35 | analytical model assumptions |
| **Table 2.1; Equation (2.5); Sections 2.2.7–2.2.8** | **28** | **36** | **target table, units, theoretical calculation, conclusions** |
| Section 1.1 | 3 | 11 | report-wide count `126 tests` (distinct from Table 2.1 rows) |
| Appendix A.1 | 103 onwards | 111 onwards | associated test matrices; individual test linkage **not yet established** |

**Visual examination:** Table 2.1 checked on rendered *physical PDF page 36*; also reviewed rendered pages 27, 29, 31–36 for units and scientific qualifications. Text extraction is supporting only.

### What Table 2.1 contains (inventory, not D3 release)

- **Two oxygen-condition rows:** 21 and 16 percent O2.
- **Three method columns:** Experiment, Computation, Theory (Equation 2.5).
- **Six reported numerical outputs:** oxygen condition × method.
- Experimental entries include **±5 mm/s** as published; no computation/theory uncertainty is explicitly shown in the table.
- **Shared conditions in the caption:** thin polymethylmethacrylate (PMMA), 1 atm; section context: low opposed forced flow in ISS microgravity.
- These are **not six independent experiments**; the table is a summary comparison between three evidence-generating methods. Neither row is demonstrated to map one-to-one to a unique on-orbit test ID.
- The full report says **126 tests performed**, vs previous **130 PSI entries**: unresolved entity/version difference, OUTSIDE this targeted table inventory.

**D1 decision:** `VERIFIED` table presence, page anchors, row/method counts and surrounding references; `UNKNOWN` per-row physical test IDs and unique sample mapping. A Table 2.1 *row* is not a `test`.

## D2 — Scientific semantics / field dictionary

The companion file `BASS_II_R5_D2_Field_Dictionary_v0.1.csv` contains stable field keys, literal source labels, raw units, data kinds, anchors, and restrictions. The required conceptual distinctions are:

1. **`V_g,cr` is a critical opposed-flow *gas velocity*, not a flame spread velocity.** In Section 2.2.5, the flame is first established in forced opposed flow and the imposed flow is reduced until steady propagation is no longer sustained / visible flame disappears. The heading relates to *radiative extinction at low opposed flow*. The spread rate `V_f` is a different field (Fig. 2.8, Eq. 2.3).
2. **Experiment** = report of an *experimentally determined extinction threshold*, with reported ±5 mm/s uncertainty. Do not tag the Table 2.1 summary value as a single direct sensor measurement or infer error distribution/meaning of ± beyond what is reported. DAP `value_kind`: `REPORTED_FINDING` with `method_origin=EXPERIMENTAL`.
3. **Computation** = output of the numerical model (2D, coupled solid/gas, with radiative modeling): DAP `DERIVED`, `method_origin=COMPUTATIONAL_MODEL`, **not a second physical measurement** (printed p. 25).
4. **Theory** = analytical/scaling result of **Equation (2.5)**: DAP `DERIVED`, `method_origin=ANALYTICAL_MODEL`, **not a third physical measurement** (printed p. 28). Treat numbers in this column as reported *model predictions*, not validated universal thresholds.
5. **Oxygen condition:** Table label `O₂, percent` is percentage, not mole fraction expressed as decimal. Conversion `21% → 0.21` is allowed only with a recorded rule (`divide by 100`); do not silently interchange `0.21` and `0.21%`. The table provides rounded/nominal oxygen conditions, not per-test gas-sensor readings.
6. **Shared pressure:** `1 atm` is caption context. Do not infer individual run pressure measurements or an uncertainty from it.
7. **Sample variations:** printed p. 21 describes PMMA sheets ~100–400 μm thick, nominally 20 mm wide; printed p. 25 says lower-O₂ tests used two thicknesses and sample widths **20 mm (100 μm)** vs **10 mm (200 μm)**. Table 2.1 does **not** identify which test/sample yields each aggregated value. Store thickness and width at table-row granularity as `UNKNOWN`, not a guessed single number.
8. **Measurement limitations:** printed p. 23 notes high error bars for low-velocity fan calibration, a time lag between adjusting flow and its arrival at the flame, and possible flow disturbance from boundary layers. ±5 mm/s in Table 2.1 cannot be assumed to cover all systematic sources independently without authors' definition.
9. **Comparability:** two O₂ rows share broad material/setup/pressure, but individual samples/test histories are not uniquely resolved from the summary table. Authors report increased critical velocity under lower oxygen, but this is a **limited reported finding**, not proof of an isolated causal effect, independent of geometry, for spacecraft materials generally.
10. **Do not merge physical metrics with FLEX:** the common layer may include `source_id`, `report_id`, `anchor`, `evidence_kind`, `units`, `QC`, `limitations`; physical comparison of BASS-II airflow with FLEX droplet diameter is invalid.

### Stable source locator proposal

`NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1|O2_21pct|method_experiment`

Use an analogous locator for the 16% row and other methods; this is a **proposed normalization convention**, not a NASA test ID. Include secondary anchors `printed_p23|PDF_p31|section_2.2.5` and `printed_p28|PDF_p36|Equation_2.5` for interpretation/derivation.

### Related scientific caution

The Section 2.2 article is identified in its printed p. 19 footnote as previously published: Bhattacharjee et al., *Combustion and Flame* 163 (2016) 472–477, DOI `10.1016/j.combustflame.2015.10.023`. This is another provenance trail, **not** a separately audited source here.

## D3–D7: NEXT, NOT DONE

**D3 intended extraction grain:** preserve **2 raw table rows** as the source table, then optionally represent **6 method-specific evidence cells** for the verifier. Every raw cell must have `raw_text`, `raw_unit`, `method`, `row_condition`, `source_anchor`, and `value_kind`; the two experimental uncertainties must be preserved as text and parsed into reported central value + `±5` only under an explicit rule. Never synthesize `test_id`.

**D4:** check each of six cells by rendered original, method provenance, units, ±5, shared constraints, and gap between reported/table and prose. No unsupported normalizations.

**D5:** reconcile Table 2.1 vs section 2.2.5, figure captions and as-run test matrices where feasible; document the two O₂ conditions' run linkage as unknown unless verified. Keep whole-project 126 vs 130 on a separate log.

**D6:** only bounded lookup, source transcription and clearly attributed within-section comparison are candidates; quantitative universal “safe flow” and Mars/Moon extrapolations prohibited.

**D7:** release only after D3–D6, immutable raw/curated/QC + manifest hashes, release ID and independently checked sample. **No BASS-II D7 release exists yet.**

## Issues / Stop conditions

- `R5-I01 HIGH`: Table 2.1 source results are summaries, not individual as-run experiment records; no test IDs.
- `R5-I02 MEDIUM`: ±5 definition and low-speed calibration limitations need fidelity in all displays.
- `R5-I03 MEDIUM`: 16% tests include differing sample thickness **and width**; avoid “controlled oxygen-only experiment” labels.
- `R5-I04 MEDIUM`: unclear redistribution of report imagery; keep attribution and provenance.
- `R5-I05 OPEN`: 126 performed tests vs previous 130 PSI entries; not reconciled.

## Mini-report / Handoff

**Source:** NASA/TM-20210011385; PSI-25 v4.  
**Version/hash:** local SHA-256 above.  
**Coverage:** Table 2.1, 2 rows × 3 methods, surrounding pp. 19–28.  
**Manual check:** original page and 6 visually inspected reported output cells, contextual figures and text.  
**D0:** identity verified; attribution/reuse caution.  
**D1:** verified targeted inventory; test linkage unknown.  
**D2:** semantic dictionary ready; no normalized source dataset produced.  
**Next single action:** D3—extract two rows/six method cells with immutable raw strings and exact locators.  
**D3 exit:** all six method cells and both reported experimental uncertainties matched to the printed table; no invented test IDs, values or missing uncertainty.
