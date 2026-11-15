# AI Assistance and Runtime Model Disclosure

**Project:** VERGE — Verified Evidence and Risk-Governed Exploration
**Event:** NASA Space Apps Challenge 2026 — Flame in Freefall
**Updated:** 15 November 2026

VERGE has **one human participant**. OpenAI **ChatGPT (GPT-6)** was used as an AI assistant to support scientific source discovery, architecture, Python and test drafts, debugging, interface text, research documentation, and submission wording. ChatGPT is **not a human or registered team participant**. The human author selected the scope, applied changes, executed local tests, made release decisions, and is responsible for the project's claims and final submission.

## What actually runs

| Component | Public Streamlit website | Optional trusted localhost |
| --- | --- | --- |
| FLEX keyword search and rank | Deterministic | Deterministic |
| FLEX/BASS-II structured claim verification | Deterministic | Deterministic |
| D7 integrity and source/QC checks | Deterministic | Deterministic |
| Gemini-generated candidate interpretations | **Disabled** | **Available only with manual local enablement and a user-supplied API key** |

The Gemini adapter uses the Google Gen AI Python SDK (`google-genai==3.3.0`, pinned in `requirements-gemini.txt`). Earlier local real API calls were reported successful by the participant; an independent R8 review exercised adapter behavior using mocks, **not** a provider connection. No custom ML model was trained by VERGE.

The local mode chooses one to four prevalidated snippets from a **single** study. FLEX D4 `REVIEW` entries are excluded from LLM intake. Gemini receives published scientific facts, source identifiers, locators and caveats. The output must use known evidence IDs and contain limitations; digits in generated prose are blocked with at most one regeneration attempt. It is always marked:

- `CANDIDATE_NOT_VERIFIED`
- `CITATION_IDS_AND_FORMAT_ONLY`

**These controls do not independently check scientific meaning.** An incorrect claim written without digits can pass the format gate. Gemini does not assign itself a NASA-EVP `SUPPORTED` verdict. The independent deterministic verifiers instead check only supported *structured* source claims, under their own rules.

## Key handling and public deployment

The local UI is gated by `VERGE_ENABLE_GEMINI_LOCAL=1` **and** a Streamlit server bound to `127.0.0.1`/`localhost`. An API key is typed into a local password field, not stored in repository source. This does **not** prove comprehensive erasure from process/browser/provider memory and does not constitute a safe public BYOK design. Never enter personal keys into untrusted public replicas. The public website does not ask visitors for an API key; there is no project-funded public inference endpoint.

If Google Gemini is later made available to the public, a separate security/cost/consent review, visitor access policy, data-handling notice and regression run are needed. No such public launch is claimed here.

## What the scientific data mean

Scientific values come from attributed NASA source reports and project-audited bounded D7 releases, not uncited free-form model assertions. NASA-DAP and NASA-EVP are **project protocols**, not official NASA certification. Their checks are not external experimental replication or spacecraft safety approval. A completed source-cell transcription check does not imply a valid fire-safety recommendation or a lunar/Mars forecast.

## Rights and submission notice

Project-original source code uses Apache-2.0. NASA reports, third-party assets and Google/OpenAI services retain their own terms. The project is independent of and not endorsed by NASA. Include both ChatGPT development assistance **and** the optional local Gemini adapter in the competition submission's AI/SI and resource fields. Any generated image/audio/video used in the actual submission must have its own appropriate disclosure and attribution; no such new asset is asserted by this file.
