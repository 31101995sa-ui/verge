# R0 — Competition, Source Rights, Branding, AI Disclosure

**Review:** 15 November 2026 · Asia/Almaty
**Project:** VERGE (one human participant; ChatGPT is an assistance tool)
**State:** public app and repository are online; **formal competition submission remains unconfirmed**.

## Competition registration and deadlines

- Official event: https://www.spaceappschallenge.org/2026/
- Challenge: https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/
- Submission instructions: https://www.spaceappschallenge.org/resources/project-submission-guide/
- Official event schedule states **15 November 2026, 23:59 in the team's registered Local Event timezone** for the Project tab. For an Almaty-registered team, that is 23:59 Asia/Almaty; **the participant must check actual team/event settings**. GitHub and Streamlit publication are **not** submission.
- Local judging and eligibility: the participant reports confirming a **15:00 Asia/Almaty local deadline/milestone** with organizers; the global online cutoff is **23:59 Asia/Almaty** for an Almaty-registered event. Verify the actual Local Event, solo participation, individual speaking slot, language/duration and any materials hand-in in the participant account. The exact individual slot and formal status were not independently inspected here.
- Seven-slide presentation and Russian script are **reported prepared by the participant**; final files, hyperlinks and access have **not** been reviewed in this documentation pass.

## Required challenge Resources — OPEN, high priority

Global Awards requirements described by the official Space Apps GO Team call for an **actually used** NASA data source listed in the selected challenge's official Resources tab. A valid NTRS or PSI URL alone does not prove membership in that specific list.

- Required page: https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/?tab=resources
- State: **NOT VERIFIED**. The independent R8 audit could not retrieve the complete list.
- Acceptance evidence: save the exact resource name and URL as displayed by the official tab, and explain which **actual** FLEX or BASS-II released field/record derives from it. Do not insert an unrelated resource merely to satisfy the form.
- If blocked, ask the local or Global Organizing Team for clarification and preserve what was actually used; continue preparing the honest submission in parallel.

## NASA sources and reuse rights

- **FLEX** — NASA/TP-2015-216046, NASA NTRS ID `20150023456`, Table IX; https://ntrs.nasa.gov/citations/20150023456. NASA NTRS metadata reported *Public Use Permitted*. Project sample: 17 source records (10 D4 VERIFIED, 7 REVIEW).
- **BASS-II** — NASA/TM-20210011385, NASA NTRS ID `20210011385`, Table 2.1; https://ntrs.nasa.gov/citations/20210011385. NTRS copyright/distribution metadata are **not** blanket permission to reuse the entire PDF, figures or video. Project release: two summary rows / six distinct method cells, not six physical tests.
- Project-original code uses [Apache-2.0](../LICENSE); NASA and third-party material retain their own rights. Sources must be cited even when publicly available. Avoid distributing original large PDFs, NASA logos or external media without confirming rights.
- **Public product brand:** VERGE only. The phrases “NASA Space Apps Challenge” and NASA report numbers are appropriate factual contest/source attribution, **not** co-branding or endorsement. Independent project; not affiliated with or endorsed by NASA.

## Scientific and AI responsibility

- NASA-DAP v1.0 and NASA-EVP v1.0 are **project-defined** quality/evidence protocols, not NASA-certified standards.
- Raw source strings, units, source IDs, missingness, anomalies and blocked uses are preserved. D4 `VERIFIED` is not an EVP `SUPPORTED` verdict. `ERROR` indicates a technical state, not a science verdict. FLEX and BASS-II remain separate physical domains. No universal safety claims or Moon/Mars extrapolation.
- **OpenAI ChatGPT (GPT-6)** helped research, architecture, code/test drafting, debugging, documentation and submission copy; the one human participant reviewed, tested and decided.
- **Google Gemini** is **implemented in the repository as an optional local-only candidate interpreter**. It requires manual flag `VERGE_ENABLE_GEMINI_LOCAL=1`, loopback `server.address`, and the user's own key. The live public dashboard is **deterministic** and requires no key. Gemini prose remains `CANDIDATE_NOT_VERIFIED` / `CITATION_IDS_AND_FORMAT_ONLY`, not source-cell scientific verification.
- Public BYOK support and server-funded API inference **are not deployed**. Do not claim complete erasure of keys from browser/provider memory or guarantee the truth of generated prose. See [AI disclosure](AI_DISCLOSURE.md).

## Public distribution / reproducibility

- [Live dashboard](https://verge-microgravity.streamlit.app/) and [GitHub](https://github.com/31101995sa-ui/verge) published.
- R9 GitHub baseline observed: [`855f4bb`](https://github.com/31101995sa-ui/verge/commit/855f4bbf9e0cf6620b29964fc4a9dff8f16f4d55). Historical R6 code + byte-exact legacy FLEX CSV fix: [`d041cbe`](https://github.com/31101995sa-ui/verge/commit/d041cbec3d097d648b8f3970e1356120194c3dfb). The participant's R6 Windows run passed **237/237**, both D7 checks and **18/18 + 10/10** benchmarks. R9 cold audit also reported the same scientific checks and full pytest PASS on a clean checkout recreated from archive `(9).rar` Git history; **no fresh GitHub network clone or cloud-side pytest was independently performed**.
- Repository `.gitignore` excludes common secrets, local `.venv` and raw PDFs; **review staged and tracked paths** because `.gitignore` cannot retroactively protect previously tracked secrets. Do not upload archives containing `.git`, `.venv`, or personal files.

## Closing state

| Area | Status |
| --- | --- |
| Scientific release identity/integrity | Verified for two bounded D7 releases |
| GitHub and public Streamlit | Published; documented workflows previously observed |
| R6 Gemini code | Published; live operation local-only; semantic verification absent |
| NASA Resources exact mapping | **OPEN** |
| Personal eligibility / local slot | **OPEN** |
| Final media/slide access | Reported prepared, **not checked** |
| Project form submission / receipt | **NOT OBSERVED** |

**R0 FULL CLOSURE: NOT YET CONFIRMED.**
