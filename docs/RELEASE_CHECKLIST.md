# VERGE — R8 Release and Submission Checklist

**R9 reviewed GitHub baseline:** `855f4bbf9e0cf6620b29964fc4a9dff8f16f4d55` (R8.1 docs) · **Scientific R6 baseline:** `d041cbe` · **Reviewed:** 15 November 2026
**Meaning of [x]:** a completed observation with the stated scope. **[ ]:** still requires a real check; not automatically satisfied by this document.

## Code, D7 and Gemini

- [x] Public source branch `main` contains the R6 Gemini modules, tests, optional SDK requirements, and Git fixes for two historical FLEX audit CSVs.
- [x] Participant's pre-commit R6 local regression: **237 tests passed**; `pip check` reported no broken requirements.
- [x] Participant's pre-commit structured benchmarks: FLEX **18/18**, BASS-II **10/10**.
- [x] Participant's pre-commit standalone FLEX and BASS-II D7 validators: **PASS**.
- [x] Source/provenance restrictions retained; no mixed FLEX/BASS-II physics, no self-awarded LLM scientific verdict.
- [x] Public Streamlit and GitHub exist and were opened during independent R8 audit (before R6 code push).
- [x] R9 cold audit: **237/237 Pytest PASS**, FLEX **18/18**, BASS-II **10/10**, both active D7 validators and Python compilation PASS in a clean checkout reconstructed from the **archived Git history** at `855f4bb`. This was **not** a fresh GitHub network clone.
- [x] `Start_VERGE.cmd` published in GitHub; the participant reported successful Windows double-click startup on a prepared `.venv` and diagnosed occupied port `8527`. No independent R9 Windows GUI test is claimed.
- [ ] Perform fresh-incognito public smoke test after the final documentation push; verify no Gemini live form or secret input on the public site.
- [ ] Review all staged/tracked files before final push; `.gitignore` alone does not guarantee secret removal.

## User experience, science and disclosure

- [x] Public deterministic workflow demonstrated: source-linked FLEX search, constrained source-cell `SUPPORTED`/`CONTRADICTED`, bounded BASS-II check, session ledger controls.
- [x] Local Gemini live candidate interpretation reported by participant, including a Russian response; no independent semantics/LLM-accuracy claim.
- [x] Local code protects against arbitrary study-mixing and limits sources to 1–4 single-study snippets; format/citation IDs and digit policy are checked.
- [x] Earlier R8 documentation polish was published in `e983cc8`; the one-click launcher and README guidance were published in `b886a22` and `855f4bb`, respectively.
- [x] R8.2 five-file documentation diff was prepared and passed isolated `git diff --check`; no Python, NASA D7, benchmarks or secrets were modified by this patch. The participant must independently confirm the Git commit/push and final staging.
- [ ] Inspect the existing English and Russian presentation files for legibility, exact links, source locators, slides count and AI disclosure. The participant says the decks are ready; their actual content has not been inspected here.
- [ ] Prepare real backup screenshots/recording if the live dashboard fails during local judging.

## Formal competition — high priority

- [ ] Log into the **actual team** Project tab; verify correct event, registration/solo status, local speaking slot, form limits, language and acceptance of terms.
- [ ] Check [Flame in Freefall Resources](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/?tab=resources) directly. Identify a **genuinely used** listed resource; record exact title/URL and evidence path. Do not claim Global Awards eligibility while this remains open.
- [ ] Provide a real accessible demo presentation/video URL, if required by the form; do not confuse app URL with the demo-asset field.
- [ ] Enter truthful English project summary, sources, tools and AI disclosures; check citations, license and unsupported fire-safety claims.
- [ ] Confirm and honor the participant-reported **local 15:00 Asia/Almaty deadline/milestone** (defense/materials) and the **online 23:59 Asia/Almaty cutoff** for an Almaty-registered Local Event; submit through the actual Project tab and save screenshot/receipt. The account-specific submitted status is not independently observed.

## Post-checkpoint scope

**Functional release is frozen at R6.** Any edit beyond documentation should require a newly evidenced blocking defect and a separate regression check. New corpus ingest, physical models, general-purpose agent planning, public Gemini BYOK and autonomous semantic verification are **out of scope for the remaining competition window**.

**CLOSE R8 ONLY WHEN:** public link and code are accessible, real slides are verified, Resources/event constraints are appropriately resolved, the project form is actually submitted, and its confirmation is saved. No checklist entry implies NASA endorsement or full scientific validation.
