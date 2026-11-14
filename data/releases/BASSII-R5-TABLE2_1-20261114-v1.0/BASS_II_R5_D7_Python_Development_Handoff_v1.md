# STELLAR ANVIL — BASS-II R5 D7 → Python Development Handoff

**Release:** `BASSII-R5-TABLE2_1-20261114-v1.0`  
**Status:** independently source-checked Table 2.1 data release, local application integration `NOT_TESTED`  
**Mode:** M2 / Stellar_Anvil_Pair_Programming_Protocol_v1.0.md  
**Source:** NASA/TM-20210011385, Table 2.1, printed p. 28 / PDF p. 36  
**Scope:** two oxygen-condition rows, six heterogeneous source results; zero uniquely mapped as-run IDs.

## Payload

- `BASS_II_R5_D7_raw_2rows_v1.csv` — byte-preserved input table rows
- `BASS_II_R5_D7_curated_6cells_v1.csv` — six method-origin evidence cells with explicit normalizations
- `BASS_II_R5_D7_QC_6cells_v1.csv` — field/method-level restrictions and unresolved linkage
- `BASS_II_R5_D7_manifest_v1.json` — release ID, SHA-256, source provenance
- `BASS_II_R5_D7_validation_check_v1.py` — standalone deterministic release checks
- `BASS_II_R5_D7_D5_Reconciliation_Log_v1.md`, `BASS_II_R5_D7_D6_Fitness_for_Use_v1.md`, `BASS_II_R5_D7_QC_and_Release_Report_v1.md`
- `BASS_II_R5_D7_proposed_claims_v1.json` — 10 **proposed** science regression cases, not verifier run results.

## One next developer action

**Inspect the current app and data-contract files**, then propose the smallest M2 addition for a *separate BASS-II Evidence Card* using the immutable D7 release. No rewrite of FLEX ingest/Explorer/verifier. Keep `source_id` and `evidence_cell_id` scoped to their investigation. Avoid reusing `flex_test_id` for BASS-II: Table 2.1 provides no unique NASA test ID.

**Version control:** The bundled D0–D2 and D3–D4 reports are historical audit snapshots; where they state “D7 not done,” this D7 report/manifest supersedes that state. Do not rerun their completed extraction without new defect evidence.

Read all CSV cells as strings; preserve `10±5` and `30±5`, not a flattened central value only. Experiments are `REPORTED_FINDING`, models `DERIVED`; display side-by-side with method labels. Oxygen 21% and 16% are nominal table conditions, not six new sensor measurements. Use 1 atm as table context.

## Scientific acceptance gates

1. Exactly 2 source table rows and 6 method-specific cells with matching QC and manifest hashes.
2. Provenance: `NASA/TM-20210011385|printed_p28|PDF_p36|Table_2.1|...` for every number.
3. `Experiment` + ±5 mm/s, distinct from `Computation` and `Theory, Equation (2.5)`; absent model uncertainty displayed as **not reported**, never zero.
4. `original_test_id` blank; no fabricated test mapping from Appendix A.1.
5. Warning: p.25 prose ~26/40 mm/s at 16% O₂, different sample widths/thicknesses, relation to tabular `30±5` unresolved.
6. Separate FIRE-SAFETY scope warning, no universal safe velocity, no Moon/Mars prediction, no pooling with FLEX droplet metrics.
7. Do not alter immutable FLEX `FLEX-R1-SAMPLE-20261114-v1.0` data or rerun prior audit without defect evidence.

## Test and handoff

From extracted folder (standard Python): `python BASS_II_R5_D7_validation_check_v1.py`. Then implement **one** M2 change, execute developer-side tests and Streamlit smoke test; report actual command output, file changes and Git hash into PROJECT_STATE. The 10 proposed claims must be explicitly integrated/tested against the existing NASA-EVP verifier before any claim of R5 verification readiness.

## Explicit bounds

D7 data release `VERIFIED` ≠ app `TESTED` ≠ claim-level NASA-EVP `SUPPORTED`. If integration is blocked, keep FLEX-only submission viable; science release need not be removed.
