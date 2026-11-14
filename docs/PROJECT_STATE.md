# Stellar Anvil — PROJECT_STATE

Project: VERGE-NASA Edition
Challenge: NASA Space Apps Challenge 2026 — Flame in Freefall
Snapshot date: 2026-11-14
Timezone: Asia/Almaty
Official participants: one human developer; ChatGPT is an AI assistant
Development mode: M2 — Accelerated Pair Programming

## CURRENT GATE

- **Active gate:** R2 — Experiment Explorer, technical implementation verified; milestone closeout in progress.
- **Next gate:** R3 — deterministic SEARCH → RANK, only after R2 state and Git are recorded.
- **R1 scientific gate:** bounded NASA-DAP D0–D7 release produced; the minimum of 10 VERIFIED source-linked point-lookup records was met.
- **R1 application integration:** locally demonstrated and committed before R2 work (last observed HEAD below).
- **Global project status:** IN DEVELOPMENT; not ready for submission.
- **Compliance note:** open R0 Resources / source-specific rights checks are not declared closed by technical progress.

## VERIFIED — LOCAL DEVELOPMENT EVIDENCE

### R0 — Bootstrap (previously observed)

- Python 3.12.10 and an activated `.venv` on the developer's Windows machine.
- Git `main`, VS Code, Streamlit bootstrap and project structure established.
- Initial Streamlit page opened in a browser.
- Previous bootstrap and compliance-documentation commits exist; current confirmed HEAD is recorded under GIT.
- These observations do not, by themselves, confirm final official Challenge Resources / licensing checks.

### R1 — Bounded FLEX D7 integration

- Release ID: `FLEX-R1-SAMPLE-20261114-v1.0`.
- Source: NASA/TP-2015-216046 / NASA NTRS `20150023456` / PSI-69.
- 17 raw, 17 curated and 17 D4/QC rows joined by unique `flex_test_id`.
- 10 records `VERIFIED` for limited source-point lookup; 7 `REVIEW`.
- Manifest-checked immutable CSV input; separate raw, curated and QC fields.
- NASA report/table/test ID, printed/PDF page, source anchor and QC restrictions preserved.
- Developer confirmed successful Streamlit display of 17 records and specific guard cases.
- Previous D7 loader regression run: 8 passed locally.
- Previous Streamlit `KeyError: flex_test_id` fixed using `set_index(..., drop=False)`; developer confirmed no recurring error.

### R2.1 — Deterministic filters

- Read-only search by FLEX ID and filters by fuel, normalized oxygen mole-fraction text, reported test end and QC status.
- Raw oxygen strings remain unchanged; curated text is used only for filter matching.
- Empty-result branch does not attempt to select a nonexistent experiment.
- Developer command: `python -m pytest -q tests/test_explorer_filters.py`.
- Observed: `7 passed in 0.84s`.

### R2.2 — Streamlit filter integration

- Filters drive both the displayed source table and selected experiment details.
- Developer performed and confirmed all requested manual UI filter scenarios.
- Developer command: `python -m pytest -q tests/test_flex_sample_loader.py tests/test_flex_d7_loader.py tests/test_explorer_filters.py`.
- Observed: `15 passed in 0.97s` after UI integration.

### R2.3 — Bounded descriptive charts

- Three Plotly categorical record-count charts: fuel, reported test end, D4 QC status.
- Charts use the currently filtered audited sample, not the entire FLEX investigation.
- An explicit UI disclaimer rejects prevalence, causal and predictive interpretation.
- Developer command: `python -m pytest -q tests/test_explorer_charts.py`.
- Observed: `7 passed in 0.85s`.
- Developer command: `python -m pytest -q tests/test_flex_sample_loader.py tests/test_flex_d7_loader.py tests/test_explorer_filters.py tests/test_explorer_charts.py`.
- Observed: `22 passed in 0.92s`.
- Browser screenshot confirmed unfiltered categorical counts:
  - Fuel: Methanol 12 / Heptane 5.
  - Reported test end: Extinction 13 / Disruption 3 / Completion 1.
  - D4 QC: VERIFIED 10 / REVIEW 7.
- Developer reported that charts work. This is a manual UI observation, not an automated Streamlit test.

## SCIENTIFIC DATA AND SCOPE

- **Dataset:** bounded 17-record sample, **not** the entire FLEX investigation or a prediction-ready benchmark.
- **NASA-DAP:** D0–D7 completed for the specified bounded release only; D5 count-entity reconciliation remains partially unresolved.
- **D6 fitness:** GO for source-linked lookup, text/category filters and explicitly bounded descriptive record counts; conditional for comparisons requiring independent comparability checks; NO-GO for causal models or safety inference.
- **FLEX-034:** preserve raw extinction droplet diameter `2` mm; numeric interpretation blocked due to Table IX / Figure 38 discrepancy.
- **FLEX-114:** preserve raw pressure `0` mmHg; pressure-dependent calculations blocked.
- **FLEX-004 / FLEX-039:** preserve distinction between raw em dash `–`, curated blank and literal numeric `0`.
- **Count entities:** 284 author-reported tests / 276 unique Table IX entries / 275 previously observed PSI records are not proven equivalent; do not treat discrepancies as errors without entity/ID reconciliation.
- **BASS-II:** not integrated; solid combustion and FLEX liquid-droplet combustion must not be pooled.
- **NASA-EVP:** independent claim verifier and evidence-ledger workflow not yet implemented; no automatic `SUPPORTED` verdicts.
- **Golden evaluation:** prespecified 10-case verification benchmark not yet executed.

## FILES — CURRENT WORKING COMPONENTS

- `app.py` — Streamlit FLEX Explorer with source/QC inspection, filters and charts.
- `src/flex_sample_loader.py` — original 9-row audit loader, retained for regression.
- `src/flex_d7_loader.py` — D7 17-row, manifest-checked raw/curated/QC loader.
- `src/explorer_filters.py` — R2 deterministic filters.
- `src/explorer_charts.py` — restricted categorical counts.
- `tests/test_flex_sample_loader.py` — initial loader tests.
- `tests/test_flex_d7_loader.py` — D7 integration tests.
- `tests/test_explorer_filters.py` — R2.1 tests.
- `tests/test_explorer_charts.py` — R2.3 tests.
- `data/audit/` — original 9-row sample and QC files (do not replace or concatenate with D7).
- `data/releases/FLEX-R1-SAMPLE-20261114-v1.0/` — D7 raw, curated, QC, manifest, validator and audit documentation.
- `docs/PROJECT_STATE.md` — this state file after developer applies and saves it.
- `README.md`, `SOURCES.md`, `.gitignore`, `requirements.txt` — project metadata and environment files.

## GIT — LAST OBSERVED DEVELOPER OUTPUT

- Branch: `main`.
- HEAD before R2 milestone commit: `848618f feat: integrate validated FLEX D7 sample into Streamlit`.
- Modified, unstaged: `app.py`, `requirements.txt`.
- Untracked R2 code/tests: `src/explorer_filters.py`, `src/explorer_charts.py`, `tests/test_explorer_filters.py`, `tests/test_explorer_charts.py`.
- Untracked audit files: seven additional legacy D0–D6 / D7 handoff and 9-row audit artifacts inside the D7 release folder, as shown by `git status --short --untracked-files=all`.
- `requirements.txt` currently differs by removing `pymupdf4llm==2.1` and `pymupdf_layout==2.1`; intent and environment implications NOT VERIFIED. Do not stage it automatically.
- R2 milestone Git commit: **PENDING — no output provided yet**.
- Remote configuration / push: NOT VERIFIED.

## OPEN ISSUES AND LIMITATIONS

- R0-001: Official Challenge Resources inclusion/cross-check not independently confirmed in this handoff.
- R0-002: Final source-specific reuse rights, third-party content, attribution and AI disclosure requirements need documented final confirmation; earlier compliance commit title is not sufficient evidence by itself.
- R1-001: D5 284/276/275 entity-level reconciliation partially unresolved.
- R1-002: Seven D7 `REVIEW` records retain field-specific restrictions; no silent status changes.
- R2-001: `PROJECT_STATE` and R2 code are not yet committed together.
- R2-002: `requirements.txt` has an unexplained removal of two packages; inspect before committing.
- R2-003: Automated Streamlit UI test not provided; manual browser checks and data-level Pytest are the available evidence.
- R3+: Search/ranking, independent verification, critique, interpretation and full benchmark remain unimplemented.

## DECISIONS

- One official human participant; ChatGPT is a supporting engineering tool.
- M2 workflow: one bounded change → exact command → observed output → Git/state checkpoint.
- Python-first stack: Streamlit, Pandas, Plotly, Pytest; PyMuPDF for source work as needed.
- FLEX first, bounded source-linked evidence; no BASS-II until permitted by quality and available time.
- Do not modify immutable D7 inputs or convert missing-value marks to zeros.
- `VERIFIED` means limited lookup eligibility, not confirmation of a causal finding.
- Descriptive categorical counts only in R2; no extinction thresholds, universal fire risks or Moon/Mars extrapolation.
- Consolidated milestone state update occurs after R2 functional verification (this snapshot).

## ONE NEXT ACTION

Apply this full document to `docs/PROJECT_STATE.md`, inspect the staged file list, and create a selective R2 Explorer milestone commit. Leave the unexplained `requirements.txt` modification unstaged until reviewed.

## EXIT CRITERIA

### R2 milestone closeout

- [x] D7 source, QC and provenance displayed in Streamlit.
- [x] ID/fuel/O₂/outcome/QC filtering demonstrated.
- [x] Three bounded categorical charts displayed.
- [x] Critical raw-value and blocked-field cases preserved.
- [x] 22 developer-side Pytest checks passed.
- [ ] `PROJECT_STATE` updated in the actual local repo.
- [ ] Selective Git commit created and its hash reported.
- [ ] Staged file inventory and residual working-tree changes reviewed.

### Next milestone

R3 — SEARCH → RANK. Begin only after the R2 closeout checkpoint has been recorded. Implement deterministic, explainable retrieval first; R4 independently verifies atomic claims under NASA-EVP.

## RELEASE STATUS

**NOT READY FOR SUBMISSION.** R2 is technically demonstrated; scientific verification pipeline, final compliance checks, end-to-end benchmark and submission remain outstanding.
