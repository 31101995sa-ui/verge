# Scientific Sources and Provenance

**Registry snapshot:** 14 November 2026 · **Project:** VERGE
**Authority:** Original NASA reports and source-linked versioned D7 releases, not LLM-generated explanations.

## Challenge and resource requirement

- [2026 NASA Space Apps Challenge — Flame in Freefall](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/)
- [Challenge Resources tab](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/?tab=resources)
- [Official project submission resources](https://www.spaceappschallenge.org/resources/project-submission-guide/)

**Pending mandatory human check:** confirm **directly in the current challenge Resources tab** that at least one source actually used by VERGE belongs to that list. The presence of a NASA NTRS or PSI URL alone does not establish membership in the challenge's particular official Resources list. This is a Global Awards eligibility requirement. Do not close this item without documentary evidence.

## FLEX — PSI-69

- **Investigation:** Flame Extinguishment Experiment (FLEX), liquid-fuel droplets, ISS microgravity.
- **Original report:** *Detailed Results from the Flame Extinguishment Experiment (FLEX), March 2009 to December 2011*, NASA/TP-2015-216046, 2015.
- **NASA NTRS record:** https://ntrs.nasa.gov/citations/20150023456 (document ID `20150023456`).
- **NASA PSI:** https://psi.nasa.gov/physci/repo/data/investigations/PSI-69.
- **Audited source:** Table IX, with explicit printed/PDF page and available Appendix B figure locators at the individual record level.
- **Local immutable release:** `data/releases/FLEX-R1-SAMPLE-20261114-v1.0/`; manifest `FLEX_R1_D7_manifest_v1.json`.
- **Coverage:** 17 selected Table IX records: D4 `VERIFIED` 10 / `REVIEW` 7. D4 status is not a scientific validation score.
- **Source limitations:** FLEX-034 reports a raw extinction diameter `2 mm` while Figure 38 indicates no extinction droplet diameter was reported; physical use is blocked. FLEX-114 contains raw `0 mmHg` ambient pressure; physical use blocked. FLEX-004/FLEX-009 missing dashes are not zero. FLEX-039's literal zero is a droplet-field value, not a zero flame diameter.
- **Open D5 issue:** 284 report tests, 276 rows in an earlier audit, and 275 earlier PSI records are not established as counts of identical entities.
- **Rights:** The NASA NTRS entry indicates **Public Use Permitted** for this report; PSI metadata licensing must not be extended automatically to report figures or third-party assets.

## BASS-II — PSI-25

- **Investigation:** Burning and Suppression of Solids-II, ISS microgravity, solid material combustion.
- **Original report:** *Burning and Suppression of Solids–II (BASS-II) Summary Report*, NASA/TM-20210011385, 2021.
- **NASA NTRS record:** https://ntrs.nasa.gov/citations/20210011385 (document ID `20210011385`).
- **NASA PSI:** https://psi.nasa.gov/physci/repo/data/investigations/PSI-25.
- **Audited source:** Table 2.1, **printed page 28 / PDF page 36**, thin PMMA, 1 atm, opposed-flow conditions. Individual method-cell source anchors are preserved.
- **Local immutable release:** `data/releases/BASSII-R5-TABLE2_1-20261114-v1.0/`; manifest `BASS_II_R5_D7_manifest_v1.json`.
- **Coverage:** 2 original oxygen-condition rows; 6 unique evidence cells, divided into **EXPERIMENTAL**, **COMPUTATIONAL_MODEL**, and **ANALYTICAL_MODEL** methods. There are **not six independent physical experiments**, and unique Appendix A.1 as-run NASA test IDs are not established.
- **Published Table 2.1 data (velocity in mm/s):**

| Nominal oxygen | Experiment | Computation | Theory |
| --- | ---: | ---: | ---: |
| 21% O₂ | 10 ± 5 | 15 | 7.5 |
| 16% O₂ | 30 ± 5 | 35 | 10 |

- **Uncertainty:** ±5 mm/s is reported for experimental entries, with no asserted statistical interpretation; model uncertainty is *not reported*, not zero.
- **Open D5 issues:** At 16% O₂, Table 2.1 lists 30±5 mm/s while Section 2.2.5 discusses approximately 26 and 40 mm/s for varying sample geometry. Their mapping is unresolved. Reported 126 tests and an earlier PSI count of 130 entries may represent different entities. Flow/calibration caveats apply.
- **Rights:** NASA NTRS currently labels the report **“Use by or on behalf of the US Gov. Permitted”**. Do **not** interpret that automatically as blanket authorization to relicense or redistribute the complete PDF, figures, or video. The project links to the report and republishes a small attributed set of scientific facts with source anchors; review any future media redistribution separately.

## Validation and audit rules

Both D7 releases have source-specific manifests with SHA-256/size validation and QC files. The active verifier revalidates evidence before assigning bounded source-transcription verdicts.

- FLEX D7: `python data/releases/FLEX-R1-SAMPLE-20261114-v1.0/FLEX_R1_D7_validation_check.py`
- BASS-II D7: `python data/releases/BASSII-R5-TABLE2_1-20261114-v1.0/BASS_II_R5_D7_validation_check_v1.py`
- FLEX 18-case benchmark: `python -m benchmarks.run_r4_benchmark`
- BASS-II 10-case benchmark: `python -m benchmarks.run_bassii_benchmark`

**Interpretation policy:** distinguish `MEASURED`, `DERIVED`, `REPORTED_FINDING`, `INFERENCE`, `UNKNOWN`; preserve raw values and original units, missingness and explicit NASA page/table/figure locators. Do not pool FLEX and BASS-II physical variables or infer general safety thresholds. NASA-EVP uses `SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`, `OUT_OF_SCOPE`; technical `ERROR` is separate from scientific verdicts.

## Attribution and data redistribution

NASA report records are authoritative for report metadata. PSI record/metadata CC0 labels, when present, do not override the permissions for linked publications, images or third-party materials. No original heavyweight NASA report PDFs, videos or official NASA marks are bundled for public distribution.

Project-original source code is governed by its [Apache-2.0 license](LICENSE). The project is independent and not endorsed by NASA.
