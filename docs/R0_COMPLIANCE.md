# R0 — Competition, Sources and Responsible AI Compliance

**Snapshot:** 2026-11-14 · Asia/Almaty
**Challenge:** NASA Space Apps Challenge 2026, *Flame in Freefall*
**Project:** VERGE; one registered human participant, AI assistant not a human teammate.

## Event and submission

- Official 2026 event: https://www.spaceappschallenge.org/2026/
- Challenge details: https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/
- Competition window: 14–15 November 2026.
- Global project submission is due **2026-11-15 23:59, participant-local time** under the official 2026 schedule. Submission occurs via the event Project Tab; a GitHub commit or Streamlit deployment is not itself a submission.
- Local Almaty event judging / mandatory attendance: **confirm directly with the local organizer**; do not substitute the global deadline for the local presentation cutoff.
- Follow current Project Submission Guide: https://www.spaceappschallenge.org/resources/project-submission-guide/.

## Required Challenge Resource — BLOCKING OPEN ITEM

NASA Space Apps GO Team states Global Awards eligibility requires **at least one NASA data source explicitly listed in the chosen challenge's Resources**. Merely citing any valid NASA report is insufficient.

- Official target: https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/?tab=resources
- Current status: **PENDING DIRECT MANUAL CONFIRMATION** for FLEX/PSI-69 and/or BASS-II/PSI-25 (or an official listed NASA source demonstrably used in the submission).
- Required evidence before R0 closure: record the exact resource title and original URL as it appears on the official tab; identify which actual VERGE dataset or finding uses it.

## Scientific sources and rights

- FLEX: NASA NTRS 20150023456, `NASA/TP-2015-216046` — NTRS **Public Use Permitted**. Reference individual report/PSI identifiers, source tables, page and figure anchors; the PSI metadata license does not automatically cover images and every linked item.
- BASS-II: NASA NTRS 20210011385, `NASA/TM-20210011385` — NTRS displays **“Use by or on behalf of the US Gov. Permitted”**, not a general CC0 report license. The public project provides links and a limited cited table of factual values; do not redistribute the complete report PDF, its figures or videos without rights review.
- Project code: Apache-2.0, see `LICENSE`; no license is asserted over NASA/third-party assets.
- Avoid NASA marks or statements of endorsement. Include "independent project; not affiliated with or endorsed by NASA" wording.
- **Public product branding:** VERGE only. The original NASA name in project-title strings is retired. Keep official NASA identifiers in citations, report titles, provenance and factual event participation; they are not product branding. Do not alter immutable NASA D7 releases or historical Git commits for cosmetic renaming.

## Source and scientific honesty

NASA-DAP v1.0 governs source identity, extraction, QC and D7 releases. NASA-EVP v1.0 governs atomized proof obligations, independent verification, counterexamples where feasible, scientific verdict and regression test. Preserve raw units, missingness, source locators and fields blocked from numerical physical use. No ISS-to-Moon/Mars inference, general fire-risk predictions or certification.

**Current implementation limitations:** BASS-II covers 6 *methods-specific* values, not independent experiments; full FLEX 284-test corpus is not incorporated. D4 `VERIFIED` remains separate from NASA-EVP `SUPPORTED`. `ERROR` denotes a technical failure and has no scientific verdict.

## AI disclosure

- OpenAI ChatGPT (GPT-6) assisted with architecture, research, code/documentation drafts, debugging and proposed test design.
- Human participant made the scientific and implementation decisions, applied changes and executed independent local tests.
- **No LLM model currently runs inside the deployed application**; no live model-generated scientific interpretation is claimed.
- Explicitly list ChatGPT among tools on the NASA project submission page and point to `docs/AI_DISCLOSURE.md`.
- Any future generated assets or LLM adapter must be individually disclosed; secrets must never be committed to the public repository.

## Security and public distribution

- `.env`, Streamlit `secrets.toml`, `.venv` and original heavyweight NASA PDF inputs excluded from tracked deliverables.
- Before GitHub public push inspect tracked files for tokens, credentials and private data; check Git commit author metadata if personal email exposure matters.
- Public page must work without API keys; current deterministic mode is designed for that.
- Repository and app URLs must be independently opened in a logged-out browser to confirm public access.

## Final R0 state

- Development after official start: locally reported, source dates align with 14 November 2026.
- Scientific-source identity: **VERIFIED within bounded releases**.
- AI disclosure: **DOCUMENTED**; submission entry pending.
- License/reuse: **LIMITED REVIEW**; BASS-II redistribution restrictions remain relevant.
- Required challenge-resource membership: **PENDING**.
- Submission and public links: **PENDING**.

**R0 FULL CLOSURE: NOT YET CONFIRMED.**
