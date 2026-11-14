# FLEX R1 · D3–D4 extension + D7 sample release v1.0

**Release ID:** `FLEX-R1-SAMPLE-20261114-v1.0`  
**Generated:** 2026-11-14T11:10:30+05:00 (Asia/Almaty)  
**Scope:** Limited and traceable subset of NASA/TP-2015-216046, *not* the full FLEX experiment repository.  
**Audit environment:** Source PDF accessed through local immutable copy; no access to developer's local Git/VS Code.

## Source and prerequisites

- Primary NASA/NTRS record: https://ntrs.nasa.gov/citations/20150023456
- NTRS ID: `20150023456`; NASA report `NASA/TP-2015-216046`, November 2015.
- Source PDF SHA-256: `b4f6ca983e2792c33a0b92220a791a818f426bb635b94f7fd33dc8c9c471e79d` (314 physical pages in PyMuPDF).
- NASA PSI investigation PSI-69: https://psi.nasa.gov/physci/repo/data/investigations/PSI-69 ; version 5 and DOI `10.60555/mbq8-0451` were visible in the official PSI listing. PSI's CC0-1.0 license does not automatically assign CC0 to the NTRS PDF; NASA NTRS labels the report `Public Use Permitted`. Cite original source; no NASA endorsement is implied.
- Official Space Apps **Resources** tab still requires project R0 cross-check.
- D0–D6 source documents used: `FLEX_R1_D0-D3_audit_v0.1.md`, `FLEX_R1_D4_QC_Report_v0.1.md`, `FLEX_R1_D5_Reconciliation_Log_v0.1.md`, `FLEX_R1_D6_Fitness_for_Use_v0.1.md`.
- Original 9-row CSV and QC CSV copied into this release **without changing their record fields**; both preserved SHA-256 values in manifest.

## D3 extension: 7 requested candidates + 1 reserve

Seven planned IDs: **FLEX-003, FLEX-005, FLEX-006, FLEX-033, FLEX-034, FLEX-035, FLEX-036**. A new candidate could not all be accepted: FLEX-034 has a contradictory source locator. A reserve **FLEX-061** was therefore audited, rather than silently accepting a questionable record.

| Experiment | Table IX location | Appendix B context | QC status | Source-specific caveat |
|---|---|---|---|---|
| FLEX-003 | Printed 20 / PDF 26 | Figure 7, printed 31 / PDF 37 | VERIFIED (point lookup) | Calibration; LLUV visibility limited |
| FLEX-005 | Printed 20 / PDF 26 | Figure 9, printed 33 / PDF 39 | VERIFIED (point lookup) | LLUV recording becomes undetectable; suspected bubble is speculative |
| FLEX-006 | Printed 20 / PDF 26 | Figure 10, printed 34 / PDF 40 | VERIFIED (point lookup) | HiBMs FOV interruption and poor LLUV settings |
| FLEX-033 | Printed 21 / PDF 27 | Figure 37, printed 61 / PDF 67 | VERIFIED (point lookup) | Color-camera images not recorded after deployment |
| FLEX-034 | Printed 21 / PDF 27 | Figure 38, printed 62 / PDF 68 | **REVIEW** | Table IX shows `2 mm` yet Figure 38 says no extinction droplet diameter is reported |
| FLEX-035 | Printed 21 / PDF 27 | Figure 39, printed 63 / PDF 69 | VERIFIED (point lookup) | Caption indicates continued post-visible-extinction vaporization suggestive of cool flames |
| FLEX-036 | Printed 21 / PDF 27 | Figure 40, printed 64 / PDF 70 | VERIFIED (point lookup) | No recorded disturbance or disruption in figure caption |
| FLEX-061 (reserve) | Printed 21 / PDF 27 | Figure 65, printed 89 / PDF 95 | VERIFIED (point lookup) | Fiber-supported, no translation; visible flame very dim |

**Method:** Each of the eight new rows was manually checked against the rendered source table on PDF pages 26–27; every cell was also checked as an exact ordered token sequence in the PDF text layer. All corresponding figure captions were read as text and visually checked in rendered PDF pages. No OCR; graphs were not digitized; no experimental value was inferred from curves. Raw strings preserve decimal notation, zeros and dashes.

### Significant cross-source finding: FLEX-034

1. NASA Table IX, printed p.21 / PDF p.27: `FLEX–034`, *Visible flame extinction diameter* = literal `2`, unit `mm`.
2. NASA Figure 38 caption, printed p.62 / PDF p.68: explicitly says **no extinction droplet diameter is reported** because the droplet left the HiBMs field of view long before visible flame extinction.
3. This is an **unresolved internal documentary discrepancy**, not proof of which passage is wrong. Keep raw `2`; mark `REVIEW`; block this metric in numeric comparisons and derived claims.

### Other caption caveats

- FLEX-003/FLEX-005/FLEX-006: calibration/LLUV visibility limits; do not treat the plotted flame curve as a perfect measured time series.
- FLEX-033: no recorded color-camera images after deployment; do not fabricate that stream.
- FLEX-035: a *visible flame* can extinguish while droplet vaporization continues; do not claim all combustion processes ceased.
- FLEX-061: fiber-supported experiment, unlike free-floating candidates; this distinction is **not** suitable for direct cross-case causal comparisons.

## D4 deterministic QC (audited sample)

| Check | Result |
|---|---|
| Source PDF accessible and matching fixed SHA-256 | PASS |
| New 8 Table IX full ordered row tokens found once on correct PDF page | PASS 8/8 |
| New 8 figure IDs/numbers/pages in Appendix B | PASS 8/8 |
| Raw output 17 records, unique IDs, exact source anchors | PASS 17/17 |
| Original nine raw rows are unchanged in exported release | PASS 9/9 |
| Original nine D4 statuses are unchanged in exported release | PASS 9/9 |
| Raw, curated and QC three-way ID join | PASS 17/17 |
| Date/GMT, fuel category, outcome and numeric lexical parsing | PASS for present values; original FLEX-009 missing GMT retained |
| Four listed gas fraction sum exactly 1.00 in current sample | PASS 17/17, arithmetic consistency **only** |
| Numeric pressure positive except known FLEX-114 | PASS per exclusion rule; `0 mmHg` retained and blocked |
| Recorded missing marks and literal zero | PASS: missing -> blank only in curated; raw preserved |
| FLEX-034 table value retained + numerical use blocked | PASS |
| QC statuses | **10 VERIFIED for point-level display / 7 REVIEW** |

**Meaning of VERIFIED:** exact Table IX row lookup, preserved reported units and values, consistent basic data types/ranges, and correct source locators. It does **not** imply that every optical diagnostic was fully reliable or that a physical hypothesis has been independently validated.

## D6 fitness retained / D7 release limits

**GO:** English-language Experiment Explorer, ID/fuel/oxygen/outcome filters, exact reported cell values and source links, missingness and QC flags, restricted non-causal descriptive display.  
**CONDITIONAL GO:** side-by-side display if material, pressure, oxygen, support fiber and measurement comparability are explicitly checked; current sample is not a scientific comparison-ready benchmark.  
**NO-GO:** generalizable extinction-threshold relationships, numerical causal analysis across unmatched conditions, universal risk score, spacecraft fire safety certification, Moon/Mars extrapolation, automatic inference of a missing or contradicted extinction diameter.

D5 differences **284 report tests / 276 Table IX rows / 275 older PSI figure** remain separate unresolved count entities. Their reconciliation is not a prerequisite for this bounded sample lookup release.

## Data release artifacts and mapping

| Artifact | Role | SHA-256 |
|---|---|---|
| `FLEX_R1_D7_raw_17row_v1.csv` | Immutable raw Table IX strings, 17 rows | `69428edf15851f753701a22e74738b517b0d480d18f2999180adade157197839` |
| `FLEX_R1_D7_curated_17row_v1.csv` | Deterministic normalized decimal layer, 17 rows, explicit block flags | `dc2aea3dfc8edae6c86bef13528e2305889673dc508754999fc0b5794e42f67e` |
| `FLEX_R1_D7_QC_17row_v1.csv` | QC flags, status, allowed and blocked use, new figure anchors | `f5910e5fdf4d5d371d00f06fc717706439b704448810c252ef7740a0385a6b9d` |
| `FLEX_R1_D7_manifest_v1.json` | Data release ID, provenance, checksums and normalization rules | (see file; manifest not self-hashed) |

**Raw** is authoritative for original NASA transcription. **Curated** derives from raw using `NORM-R1-V1`: decimal parsing without unit conversion; `–` -> blank/unknown only in curated; `0` remains `0`. The `visible_flame_extinction_droplet_diameter_mm` column means **droplet**, not flame diameter. D4 status is a record-level lookup clearance; column-level blocked fields must also be honored.

## Current gate / handoff decision

- **D7 output:** limited 17-row dataset released in audit workspace with DAP exceptions and hashes. 
- **R1 scientific minimum:** ≥10 source-linked point-lookup VERIFIED records is met (10). This does **not** remove seven REVIEW items or global count disagreements.
- **R1 application gate:** developer must import, independently reproduce QC statuses and commit in local repo; this is not yet evidenced here. The source data have not been copied into the developer's Git or run on their computer.
- **ONE NEXT ACTION:** deliver the D7 artifacts and verify a read-only loader/Explorer in the Python Development chat; then update `PROJECT_STATE` with the real command output and commit.
- **EXIT CRITERION:** local loader reads 17 raw records, 17 curated records, 17 QC entries; 10 VERIFIED/7 REVIEW; source pointers and blocked fields survive unchanged; recorded passing test and Git commit.
