# PROJECT_STATE — VERGE-NASA Edition

**Snapshot date:** 2026-11-14 · **Timezone:** Asia/Almaty
**Scope:** Phase B.2 deployment-readiness preparation, after R5.3 and Scientific Mission Control UI.

## CURRENT GATE

**Phase B.2 — reproducible public-deployment package; not yet deployed.** The previous Phase A Scientific Mission Control UI is locally functional. Phase C GitHub / public Streamlit URL and optional runtime LLM are separate, uncompleted gates.

## VERIFIED (actual observations)

- Git HEAD in the uploaded archive: **`906e1ca`**, `feat: integrate BASS-II verification and Mission Control UI` (35-file milestone).
- Archived working-tree source independently executed under Python: **206/206 Pytest PASS**, FLEX 18/18 scientific benchmark, BASS-II 10/10 benchmark. **A separate clean clone of HEAD `906e1ca` failed BASS-II hash checks because Git had normalized CRLF bytes in two source CSVs; this is the specific issue the Phase B.2 `.gitattributes` and byte-preserving Git restaging must fix.**
- Standalone FLEX D7 validator PASS (17 unique records, 10 `VERIFIED`, 7 `REVIEW`, immutable CSV hash checks).
- Standalone BASS-II D7 validator PASS (2 source rows; 6 method-specific cells; 6 QC matches; raw string and unit/uncertainty checks).
- Human developer previously confirmed the UI's six-tab layout, correct `app.py` SHA-256, Pytest 206/206, FLEX 18/18 and BASS-II 10/10 locally.
- No successful GitHub push, clean remote clone, fresh cloud installation or public browser smoke test has been observed.

## IMPLEMENTED

- **R1 FLEX D7**: NASA/TP-2015-216046 Table IX, 17 bounded source-linked records, raw/curated/QC, D0–D7 manifests and restrictions.
- **R2 Explorer**: filters, source inspection, categorical composition and localized Plotly charts.
- **R3 Search/Rank**: deterministic lexical retrieval and explainable relevance scores; not scientific confidence.
- **R4 FLEX EVP**: structured source-cell/scope verification, constrained English Table IX parser with human confirmation, session Evidence Ledger and JSON export. Technical `ERROR` is separate from a scientific verdict.
- **R5 BASS-II D7**: NASA/TM-20210011385 Table 2.1, 2 nominal O₂ conditions, 6 distinct method-specific values, manifest validation and separate structured verification / Evidence Ledger.
- **Phase A Scientific Mission Control**: dark native Streamlit theme, Overview/Explore/Search/Verify/Evidence Ledger/Methods navigation, EN/RU display without translating NASA identifiers or units.

## NOT IMPLEMENTED / NOT YET VERIFIED

- **R6**: no runtime LLM API/adapter, no automatic free-form source-grounded synthesis/interpretation, no autonomous counterexample search; an LLM cannot self-issue NASA-EVP `SUPPORTED`.
- **R7**: frozen 18 FLEX and 10 BASS-II case suites are verified, but comprehensive public-browser/cold-clone testing, unqualified baseline comparisons, and all acceptance evidence are not complete.
- **R8**: no public URL, verified GitHub repo, recorded demo, final presentation or submission receipt.
- **R0**: NASA 2026 challenge *Resources* membership for a source actively used by the project remains **PENDING DIRECT VERIFICATION**; current reuse/attribution and AI disclosures documented but must be reviewed for submission.

## SCIENTIFIC RESTRICTIONS

FLEX is droplet combustion; BASS-II is solid-fuel combustion. Never merge their physics quantitatively. D4 QC `VERIFIED` is not NASA-EVP `SUPPORTED`. Distinguish raw literals (`0`, `–`, blank) and missingness. NASA/TP FLEX-034/114 remain restricted. BASS-II method categories (`EXPERIMENTAL`, `COMPUTATIONAL_MODEL`, `ANALYTICAL_MODEL`) and ±5 experimental uncertainty stay distinct; model uncertainty is not reported. BASS-II Table 2.1 versus §2.2.5, and unique as-run test ID mapping, remain unresolved. No Moon/Mars partial-gravity prediction, general safe ventilation threshold or certification is permitted.

## FILES + COMMIT

- Last verified Git HEAD from archive: **`906e1ca`** (branch `main`).
- Phase B.2 package proposes documentation, `.gitignore` and minimal deployment dependencies only. **Not committed in the developer's repository**.
- Raw D7 CSVs and scientific manifest contents must remain byte-identical.
- Archive included seven optional historical FLEX audit files not tracked by Git; evaluate separately rather than bulk-staging.
- Archive included an accidental-looking untracked file with a pasted Git command in its filename; verify before deleting or staging.
- Archived `requirements.txt` had two unexplained removed optional PDF processing pins; Phase B.2 proposes a minimal, explicit runtime dependency list rather than reintroducing unused PDF libraries.
- Archived Git metadata had no configured remote. Do not imply GitHub publication.
- **Cold-clone blocker discovered in Phase B.2:** the published Git blobs of two BASS-II CSVs and two historical FLEX audit CSVs contained LF-normalized bytes rather than their SHA-256-verified working-tree CRLF bytes. Stage the unchanged original bytes under `.gitattributes` with `-text` before GitHub publication. This is a repository transport fix, not a scientific data correction.

## RELEASE POLICY

1. Protect the known-good `906e1ca` baseline.
2. Commit Phase B.2 documentation/configuration in a **separate selective commit** after local test run.
3. Before publication inspect Git tracked files for credentials and personal author metadata; `.gitignore` is not a guarantee against already-tracked secrets.
4. Deploy from reviewed GitHub `main` with `app.py` entrypoint and Python **3.12** via Streamlit Community Cloud.
5. Confirm actual public URL and repeat 11 browser scenarios in a fresh session before release freeze.
6. Conditional R6 LLM work only **after** public deployment and separate approval; deterministic verification remains the baseline.

## ISSUES

1. **BLOCKER until fixed in Git:** clean clone of `906e1ca` corrupts byte-exact BASS-II CSV payloads via line-ending normalization; four unchanged source CSV blobs must be recommitted under `.gitattributes`.
2. Current cloud install of minimized requirements not independently cold-tested; Linux/Python 3.12 build is pending.
3. Official Challenge Resources membership and final competition project-submission requirements need direct page review.
4. Legacy FLEX audit files are untracked; don't accidentally publish them.
5. The source archive had widespread LF/CRLF Git noise; check `git diff --ignore-space-at-eol` before interpreting widespread changes.
6. Public demonstration / links / submission are not complete.

## ONE NEXT ACTION

Install the Phase B.2 package and `.gitattributes`; stage the **four original, byte-identical scientific CSVs** which Git previously normalized, while leaving their working-tree values untouched. Run the D7 validators and 206 tests in a **fresh Git clone** of the corrected commit as well as locally. Only then approve GitHub publication.

## EXIT CRITERION

- Phase B.2: new documentation accurately describes R1–R5/Phase A; minimal dependencies and developer-test setup are coherent; D7 immutable and byte-preserved in Git; local **and clean-clone** tests green; selective Git commit and its hash observed.
- Phase C: GitHub repository published and accessible; Streamlit URL opened successfully in an independent browser; source and verifier behavior checked end-to-end.

**SUBMISSION STATUS: NOT YET RELEASE CANDIDATE.**
