# Stellar Anvil — PROJECT_STATE

Project: VERGE-NASA Edition  
Challenge: NASA Space Apps Challenge 2026 — Flame in Freefall  
Snapshot date: 2026-11-14  
Timezone: Asia/Almaty  
Official participant: one human developer; ChatGPT is an AI assistant  
Development mode: M2 — Accelerated Pair Programming

## CURRENT GATE

- **R0:** Development bootstrap completed. Formal official Challenge Resources, permissions, attribution and submission compliance review remains open.
- **R1:** Bounded NASA-DAP D0–D7 FLEX sample released and integrated.
- **R2:** Explorer implementation, regression and browser display completed; Git commit `b5d8ac8`.
- **R3:** Deterministic retrieval, explainable rank and Evidence Search UI implemented; Git commit `9ca81cd`.
- **R4.1–R4.5:** Structured source transcription, field restrictions, Decimal unit equivalence, scientific scope guards and 18-case pre-registered benchmark implemented and tested locally.
- **R4.6:** Streamlit Evidence Verification and session Evidence Ledger integrated. After an unsaved-file/duplicate-tail incident, developer reports corrected file and passing tests; a complete seven-scenario browser checklist and R4 Git commit have not been supplied.
- **Next bounded feature:** R4.7, a strictly constrained, fail-closed English transcription parser; not general natural-language verification.
- **Global status:** IN DEVELOPMENT; **NOT READY FOR SUBMISSION**.

## VERIFIED — DEVELOPER-SIDE EXECUTION

- Python 3.12.10, `.venv`, Streamlit, Pandas, Plotly, Pytest, Git and VS Code established earlier.
- R2 final local regression: `22 passed in 1.12s`, followed by Git `b5d8ac8`.
- R3 retrieval and ranking final local regression: `39 passed in 1.41s`; Streamlit Evidence Search manually confirmed working; Git `9ca81cd`.
- R4.1 local: `48 passed in 1.70s` including nine oxygen-verifier tests.
- R4.2 local: `62 passed in 1.94s` including 14 field-block tests.
- R4.3a local: `73 passed in 2.19s` including 11 unit-conversion tests.
- R4.3b local: `87 passed in 2.26s` including 14 scope-guard tests.
- R4.4–R4.5 local: `102 passed in 2.78s`, 15 new tests; `python -m benchmarks.run_r4_benchmark --output artifacts/r4_benchmark_v0.1.json` produced **18/18 PASS** with 17 scientific verdicts and one simulated technical `ERROR` / no verdict.
- R4.6: developer reported `115 passed in 3.41s` during debugging; that same run did not guarantee valid `app.py` (unsaved changes). Developer subsequently explicitly reported that the file was saved, duplicate entry point removed, and tests passed. Exact later stdout and complete browser verification not independently observed in this chat.
- Independent Python prototype results are supplementary only; local developer results above are authoritative for project status.

## SCIENTIFIC RELEASE / DATA PROVENANCE

- Release: `FLEX-R1-SAMPLE-20261114-v1.0` (immutable 17-record FLEX sample; not the entire investigation).
- Source: NASA/TP-2015-216046; NTRS `20150023456`; FLEX PSI-69; Table IX with experiment ID, printed/PDF pages, raw/curated/QC source anchors.
- D4 statuses: 10 `VERIFIED` **for limited lookup**, 7 `REVIEW`; neither is a NASA-EVP claim verdict.
- FLEX-034: raw extinction-droplet diameter `2` mm; Table IX versus Figure 38 documentary conflict; physical numeric use blocked.
- FLEX-114: raw ambient pressure `0` mmHg; physical pressure analysis blocked.
- FLEX-004 / FLEX-009: source `–` is missingness, not numerical zero.
- FLEX-039: source literal `0` retained but extinction-diameter interpretation blocked.
- D5 count entities: author-reported 284 tests, 276 Table IX rows, older PSI count 275; reconciliation partially unresolved, not confirmed NASA errors.
- Only bounded source-cell claims can receive `SUPPORTED`; no universal causal/threshold claims, spacecraft safety certification, fire-risk prediction or Moon/Mars extrapolation under this release.
- BASS-II / PSI-25: not integrated into the active FLEX verifier; do not mix physically non-comparable studies.

## R4 EVIDENCE CONTRACT

- Contract: `FLEX_R3_R4_Evidence_Contract_v0.1.md`; scientific cases: `FLEX_R3_R4_Proposed_Claims_v0.1.json`.
- NASA-EVP verdicts: `SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`, `OUT_OF_SCOPE`; technical `ERROR` is separate and has no verdict.
- Structured router does not parse free-text claims. Statement classes are selected explicitly by the caller.
- Reported source-cell values and source units are compared deterministically using Decimal and bounded supported conversions.
- Blocked fields remain discoverable and may support **literal transcription only** with QC warnings; numerical physical interpretation abstains.
- R4.5 expected statuses were predeclared. Local benchmark **18/18 PASS** demonstrates those cases only; not exhaustive scientific correctness.
- R4.6 session ledger exports observed structured claims, proof checks, verdicts and source anchors as JSON. In-memory until exported; not cryptographically tamper-proof.
- `claim_text = null`, `counterexamples_checked = false` and no LLM verification for current R4.6.

## CURRENT WORKING FILES

- `app.py`: Streamlit R2 Explorer, R3 Evidence Search and R4.6 Verification UI.
- `src/flex_d7_loader.py`: manifest-checked release loader.
- `src/explorer_filters.py`, `src/explorer_charts.py`: bounded filtering and charts.
- `src/retrieval.py`, `src/ranking.py`: deterministic lexical source-linked retrieval/rank.
- `src/evidence_verifier.py`, `src/field_evidence.py`: source-cell checks, missingness and QC gates.
- `src/unit_rules.py`, `src/scope_gate.py`: Decimal unit conversion and restricted scope policy.
- `src/claim_router.py`: structured NASA-EVP dispatch with independent release validation.
- `src/evidence_ledger.py`, `src/verification_ui.py`: session ledger and Streamlit verification panel.
- `benchmarks/r4_claim_inputs.py`, `benchmarks/run_r4_benchmark.py`, `benchmarks/FLEX_R3_R4_Proposed_Claims_v0.1.json`: frozen scientific scenarios and runner.
- `tests/`: previously executed loader, explorer, retrieval, ranking, verification, scope, benchmark and ledger regression tests.
- `artifacts/r4_benchmark_v0.1.json`: developer-produced observed benchmark report; ensure it is preserved, but do not confuse it with the frozen benchmark input fixture.
- `data/releases/FLEX-R1-SAMPLE-20261114-v1.0/`: immutable scientific inputs and QC documentation.

## GIT — OBSERVED

- Branch `main`; last confirmed HEAD: `9ca81cd feat: complete FLEX R3 evidence search and ranking`.
- R4 source/tests/app have **not** been confirmed committed.
- Last known unrelated working-tree changes: `requirements.txt` modification removing `pymupdf4llm` and `pymupdf_layout` pins (reason unverified); seven legacy audit artifacts untracked under the D7 release folder.
- Remote / push status: NOT VERIFIED.
- Preserve R4 benchmark report. Review `.gitignore` and artifact disposition before staging generated outputs.
- Do not use `git add .` until unrelated changes have been reviewed.

## OPEN ISSUES

1. Final official Challenge Resources, use permissions, attribution, AI disclosure, and submission/demonstration requirements require current evidence-based R0 check.
2. R4.6 seven-scenario browser smoke test not fully evidenced in local output; user reported corrected UI source and successful testing.
3. R4 code and documentation not yet selectively committed; `PROJECT_STATE` local update pending.
4. Current source-linked sample is 17 selected records and unfit for generalizable physical comparisons; D5 entity/count reconciliation remains open.
5. Free-English claims, independent counterexample search, richer interpretation and durable server ledger are not implemented.
6. `requirements.txt` unexplained diff and seven untracked legacy audit files require separate disposition.
7. No complete submission, presentation/demo recording or official submission confirmation has been observed.

## DECISIONS

- One official participant; AI assistance disclosed in source/documentation as applicable.
- M2: one bounded change, full visible code, exact local test command and actual output, state plus Git checkpoint.
- Do not rewrite completed scientific D7 CSV/manifest or silently normalize anomalous values.
- Never derive NASA-EVP `SUPPORTED` from R3 ranking or D4 `VERIFIED` alone.
- English app/README/submission; Russian internal technical collaboration and local verbal defense permitted where locally confirmed.
- For R4.7 accept only strict source-transcription templates; reject ambiguous/free-form causal statements; show structured fields for confirmation; verifier always decides the claim status.

## ONE NEXT ACTION

1. Apply this state snapshot to `docs/PROJECT_STATE.md`, complete the R4.6 local browser checklist if not already done, and create a **selective R4 milestone Git commit** (R4 files, benchmark fixture, and state only; keep unrelated dependency/audit changes separate).
2. Then begin R4.7 narrow English source-transcription parsing with a dedicated new module and tests; do not silently pass unsupported text as validated.

## EXIT CRITERION

- R4 closeout: `python -m py_compile app.py` succeeds; 115 existing tests pass after saved change; 18/18 benchmark reconfirmed; structured verification UI and JSON export demonstrated; selective Git commit and actual hash reported.
- R4.7 parser: only explicitly supported single-claim Table IX patterns produce a candidate with source locator; unsupported/ambiguous assertions abstain; separately executed source verifier produces scientific verdict; regression suite remains green.
- Global submission readiness remains **NOT VERIFIED** until R7/R8 deliverables and compliance checks are completed.

## RELEASE STATUS

**NOT READY FOR SUBMISSION** — implemented source-linked evidence exploration and bounded deterministic verification require final UI/compliance/packaging closure.
