# PROJECT_STATE — VERGE

**Snapshot:** 15 November 2026 · Asia/Almaty
**Basis:** observed published GitHub `main` commit [`855f4bbf9e0cf6620b29964fc4a9dff8f16f4d55`](https://github.com/31101995sa-ui/verge/commit/855f4bbf9e0cf6620b29964fc4a9dff8f16f4d55), earlier archive `(7).rar` comparison, participant's Windows acceptance reports, and the Mission Control R9 cold-audit handoff for archive `(9).rar`. The `(9).rar` audit results are reported in that handoff; the archive was not independently re-opened in this R8.2 pass.
**Mode:** M2; documentation-only R8.2 consistency pass; no changes to scientific releases or algorithms.

## CURRENT GATE

**R8.2 — final documentation consistency and competition defense preparation; scientific functionality frozen at R6 (`d041cbe`).** R9 audited documentation/launcher checkpoint: `855f4bb`. The public deterministic dashboard is online; Gemini source code is published, but live Gemini remains **local-only**. An official project submission receipt has not been observed.

## VERIFIED / OBSERVED

| Check | Evidence and qualification |
| --- | --- |
| R9 published GitHub baseline | The repository `main` was independently read at **`855f4bb`** on 15 November 2026; this documents the remote HEAD, not the current local working-tree status |
| Earlier archive `(7).rar` vs R6 GitHub | 97 tracked files: 62 byte-identical and 35 CRLF/LF-only differences in the earlier `d041cbe` comparison; no substantive code/science differences observed in that comparison |
| Participant's local R6 tests | `python -m pytest -q` **237 passed**; `pip check` no broken requirements |
| Active NASA-DAP D7 | Standalone FLEX and BASS-II validators both PASS; source data files and manifests retained unchanged |
| Structured benchmark | FLEX **18/18 PASS**; BASS-II **10/10 PASS** (including deliberate false and out-of-scope cases) |
| Published web app | https://verge-microgravity.streamlit.app/ opened and completed bounded public workflows during Work's earlier R8 audit; subsequent deploy availability still needs a final browser smoke test |
| R6 Gemini | Human reported a successful real Gemini source-grounded response and Russian candidate output; Work's archive tests used mock clients; no live provider call was independently rerun in that audit |
| Legacy audit CSV Git fix | Two historical `data/audit` blobs were restaged byte-exactly in the R6 commit `d041cbe`; the subsequent R9 archived-history clean-checkout run passed the full regression. |
| R9 cold audit (reported by Mission Control) | **237/237 Pytest PASS**, FLEX **18/18**, BASS-II **10/10**, both active D7 validators PASS and Python compilation PASS, using a clean checkout reconstructed from archive `(9).rar` Git history; **not** a fresh GitHub network clone |
| Windows one-click launcher | `Start_VERGE.cmd` is published and uses prepared `.venv`, loopback `127.0.0.1:8527`, and local-only Gemini flag. The participant reported successful double-click startup and diagnosed the occupied-port behavior; an independent Windows GUI execution was not performed in R9. |

Mission Control is refreshing English and Russian seven-slide decks; **the resulting slide files and public demo link have not been independently inspected in this documentation pass**. Do not claim presentation QA or official submission is complete.

## IMPLEMENTED (BOUNDED)

- **R1 / NASA-DAP FLEX:** 17 selected Table IX source records, 10 D4 `VERIFIED`, 7 D4 `REVIEW`, exact raw values, QC flags and source anchors.
- **R2:** filterable FLEX explorer, descriptive plots and study-specific BASS-II source card.
- **R3:** transparent lexical search and ranking for FLEX only (not scientific-confidence ranking).
- **R4 / NASA-EVP FLEX:** structured field/scope checks; constrained English claim intake; source-linked verdicts; session-only JSON evidence ledger.
- **R5 / NASA-DAP BASS-II:** two Table 2.1 oxygen rows, six distinct method-specific cells; independent source verification and ledger.
- **Scientific Mission Control UI:** six tabs, EN/RU interface, integrity checks, provenance and caveats.
- **R6 Gemini:** local candidate generation for 1–4 integrity-checked snippets from one study; FLEX `REVIEW` excluded; JSON structure/citation-ID checks, digit gate with one retry, explicit limitations and `CANDIDATE_NOT_VERIFIED`. The published repository contains these source modules; the public cloud UI **does not enable live Gemini**.
- **R8.1 launcher:** published `Start_VERGE.cmd` launches the local application by double-click on a **prepared Windows environment** with `.venv`. It binds to `127.0.0.1:8527`, enables local Gemini, warns about missing dependencies/occupied port, and does not distribute Python or API credentials. This is not a portable installer or standalone EXE.

## LIMITATIONS / NOT IMPLEMENTED

- No semantic independent verification of arbitrary Gemini prose, autonomous counterexample search, or full V0–V6 NASA-EVP chain for free text.
- No full NASA combustion corpus search; no uncontrolled cross-study synthesis, general safety thresholds, physical prediction, Moon/Mars extrapolation or equipment certification.
- FLEX and BASS-II describe different physics; D4 `VERIFIED` is not the scientific verdict `SUPPORTED`, and technical `ERROR` is not a verdict.
- FLEX-034 Figure 38/Table IX, FLEX-114 raw pressure, missingness/zero distinctions, BASS-II Table 2.1 versus §2.2.5 and unmapped as-run IDs remain restricted/unresolved.
- Local Gemini key handling is a convenience for trusted localhost use, not a public security guarantee; no visitor BYOK or server-funded open API is deployed.

## FILES + COMMIT

- **R9 published baseline observed:** `855f4bb` (R8.1 README launcher documentation). Historical checkpoints: `d041cbe` (R6 science/code + Gemini), `e983cc8` (R8 documentation), `b886a22` (Windows launcher).
- **R8.2 documentation scope:** `README.md`, `docs/PROJECT_STATE.md`, `docs/RELEASE_CHECKLIST.md`, `docs/DEPLOYMENT.md`, `docs/R0_COMPLIANCE.md`. The resulting Git checkpoint is determined by repository history; this snapshot does not pre-claim a commit or push.
- Earlier archive `(7).rar` contained seven untracked historical FLEX support files and an accidental console-named file; current local working-tree status **has not been inspected** in R8.2. Do not stage extras indiscriminately.
- Public runtime `requirements.txt` contains Streamlit, pandas, Plotly. The optional SDK remains separate in `requirements-gemini.txt` (`google-genai==3.3.0`).

## ISSUES / BLOCKERS

**P0 for competition acceptance:** verify a genuinely used NASA item in the *official challenge Resources* list; confirm the registered Local Event and any remaining solo/individual-slot conditions; validate the actual accessible demo/presentation link; manually submit Project page and retain confirmation. The participant reports a local deadline/milestone at **15:00 Asia/Almaty**; the global online cutoff is **23:59 Asia/Almaty** for an Almaty-registered event. Account-specific completion has not been observed.

**P1 before presentation:** review the refreshed EN/RU decks in their actual final formats; perform final incognito public smoke test. A fresh *network* GitHub clone was not observed, although R9 clean-checkout-from-archive tests passed. Review the final documentation diff and staged files for accidental credentials or audit scraps.

**Not a blocker requiring new code:** local Gemini prose may be semantically wrong while passing citation/format checks; preserve the candidacy label and describe that limitation accurately.

## ONE NEXT ACTION

Apply the five-file R8.2 documentation consistency patch, inspect the exact diff, and create a selective docs-only commit. Then return to Mission Control for defense/submission freeze; do not add functionality.

## EXIT CRITERION

R8.2 closes when the reviewed documents match R9 release reality without stale current-status claims, source/code/D7 remain unchanged, and the human verifies the docs-only Git checkpoint. Competition submission closes separately only after actual Resource/event checks, accessible demo files and an observed official submitted status/receipt.

**SUBMISSION STATUS: NOT YET INDEPENDENTLY CONFIRMED.**
