# PROJECT_STATE — VERGE

**Snapshot:** 15 November 2026 · Asia/Almaty
**Basis:** published GitHub `main` commit [`d041cbec3d097d648b8f3970e1356120194c3dfb`](https://github.com/31101995sa-ui/verge/commit/d041cbec3d097d648b8f3970e1356120194c3dfb), submitted local archive `(7).rar`, participant's R6 command outputs, and R8 Work audit.
**Mode:** M2; documentation-only release polish; no changes to scientific releases or algorithms.

## CURRENT GATE

**R8 — documentation polish and competition submission preparation; functional release frozen at R6 (`d041cbe`).** Public deterministic VERGE is online. Gemini code is published and tested locally but its live UI is **local-only**. An official project submission receipt has not been observed.

## VERIFIED / OBSERVED

| Check | Evidence and qualification |
| --- | --- |
| Local Git → GitHub | `git push origin main` succeeded; local `HEAD` and `origin/main` matched `d041cbe` in participant output; independent repository tree showed the same SHA |
| Archive versus GitHub | 97 tracked files: 62 byte-identical and 35 CRLF/LF-only differences; no substantive differences in code/scientific values in the archived comparison |
| Participant's local R6 tests | `python -m pytest -q` **237 passed**; `pip check` no broken requirements |
| Active NASA-DAP D7 | Standalone FLEX and BASS-II validators both PASS; source data files and manifests retained unchanged |
| Structured benchmark | FLEX **18/18 PASS**; BASS-II **10/10 PASS** (including deliberate false and out-of-scope cases) |
| Published web app | https://verge-microgravity.streamlit.app/ opened and completed bounded public workflows during Work's earlier R8 audit; subsequent deploy availability still needs a final browser smoke test |
| R6 Gemini | Human reported a successful real Gemini source-grounded response and Russian candidate output; Work's archive tests used mock clients; no live provider call was independently rerun in that audit |
| Legacy audit CSV Git fix | Two `data/audit` blobs were restaged without line-ending normalization under `.gitattributes`; their canonical Git blobs are included in `d041cbe`. A new cold-clone full pytest run remains to be recorded. |

The participant reports that English and Russian slide decks are prepared. **Deck files have not been inspected in this documentation iteration; do not claim they passed presentation QA.**

## IMPLEMENTED (BOUNDED)

- **R1 / NASA-DAP FLEX:** 17 selected Table IX source records, 10 D4 `VERIFIED`, 7 D4 `REVIEW`, exact raw values, QC flags and source anchors.
- **R2:** filterable FLEX explorer, descriptive plots and study-specific BASS-II source card.
- **R3:** transparent lexical search and ranking for FLEX only (not scientific-confidence ranking).
- **R4 / NASA-EVP FLEX:** structured field/scope checks; constrained English claim intake; source-linked verdicts; session-only JSON evidence ledger.
- **R5 / NASA-DAP BASS-II:** two Table 2.1 oxygen rows, six distinct method-specific cells; independent source verification and ledger.
- **Scientific Mission Control UI:** six tabs, EN/RU interface, integrity checks, provenance and caveats.
- **R6 Gemini:** local candidate generation for 1–4 integrity-checked snippets from one study; FLEX `REVIEW` excluded; JSON structure/citation-ID checks, digit gate with one retry, explicit limitations and `CANDIDATE_NOT_VERIFIED`. The public cloud UI **does not enable live Gemini**.

## LIMITATIONS / NOT IMPLEMENTED

- No semantic independent verification of arbitrary Gemini prose, autonomous counterexample search, or full V0–V6 NASA-EVP chain for free text.
- No full NASA combustion corpus search; no uncontrolled cross-study synthesis, general safety thresholds, physical prediction, Moon/Mars extrapolation or equipment certification.
- FLEX and BASS-II describe different physics; D4 `VERIFIED` is not the scientific verdict `SUPPORTED`, and technical `ERROR` is not a verdict.
- FLEX-034 Figure 38/Table IX, FLEX-114 raw pressure, missingness/zero distinctions, BASS-II Table 2.1 versus §2.2.5 and unmapped as-run IDs remain restricted/unresolved.
- Local Gemini key handling is a convenience for trusted localhost use, not a public security guarantee; no visitor BYOK or server-funded open API is deployed.

## FILES + COMMIT

- **Scientific/code baseline:** `d041cbe` (`main`, already pushed).
- **Documentation package proposed:** `README.md`, `SOURCES.md`, `docs/PROJECT_STATE.md`, `docs/AI_DISCLOSURE.md`, `docs/R0_COMPLIANCE.md`, `docs/DEPLOYMENT.md`, `docs/RELEASE_CHECKLIST.md`. These changes require the participant's separate review, copy, tests and documentation commit.
- Seven additional historical FLEX files remain untracked under `data/releases/FLEX-R1-SAMPLE-20261114-v1.0/`, along with an accidentally named local console file; exclude both from indiscriminate staging.
- Public runtime `requirements.txt` contains Streamlit, pandas, Plotly. Optional local model SDK is pinned separately in `requirements-gemini.txt` (`google-genai==3.3.0`).

## ISSUES / BLOCKERS

**P0 for competition acceptance:** verify an actually used NASA item in the *official challenge Resources* list; confirm current local-event submission/solo rules and deadlines; validate accessible demo/presentation link; manually submit Project page and retain confirmation.

**P1 before presentation:** review two existing decks in their actual final formats and test readability/links; perform final incognito public smoke test; run full pytest in a fresh checkout of published `main` (post-FLEX Git fix); update public documents without accidentally publishing credentials or optional audit scraps.

**Not a blocker requiring new code:** local Gemini prose may be semantically wrong while passing citation/format checks; preserve the candidacy label and describe that limitation accurately.

## ONE NEXT ACTION

Apply the documentation-only polish package, run agreed checks, and create a selective documentation commit. Then finish official Resources mapping and submission/rehearsal, not new functional development.

## EXIT CRITERION

Documentation matches published R6 boundaries; no source/code/D7 changes; GitHub updated by a verified docs-only commit; actual presentation and public link checked; event and Resources requirements resolved or disclosed accurately; official submitted status/receipt observed.

**SUBMISSION STATUS: NOT YET INDEPENDENTLY CONFIRMED.**
