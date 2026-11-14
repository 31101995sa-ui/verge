# VERGE — Verified Evidence and Risk-Governed Exploration

**Scientific Mission Control for evidence-linked microgravity combustion research**
**NASA Space Apps Challenge 2026 · Flame in Freefall**
**Stellar Anvil · independent participant project (not an official NASA product)**

**VERGE** expands to **Verified Evidence and Risk-Governed Exploration**. In this project, "risk-governed" means guarding against unsupported scientific claims, bad source attribution, data-quality anomalies and extrapolation beyond the evidence — **not** predicting physical fire risk.

The product is called **VERGE**. NASA is an attributed source of research data and the organizer of the Space Apps Challenge, **not** a co-developer, endorser or part of the product brand.

VERGE is a bilingual (English/Russian) Streamlit research dashboard for **looking up, exploring, searching, and checking bounded claims** against NASA combustion reports. It is designed around a traceable chain from a published observation to a source locator, quality restriction, and independent deterministic verification.

**Project status (14 November 2026):** Scientific Mission Control UI, FLEX R1–R4 and bounded BASS-II R5.3 are implemented and tested locally. **Public deployment and an in-app LLM interpretation adapter are not yet implemented/verified.** The broader intended workflow, `SEARCH → SUMMARIZE → RANK → INTERPRET → VERIFY → CRITIQUE`, is not fully automated by the current release.

## Open the dashboard

When deployed, the app should be available at a public Streamlit URL. **No public URL has been verified yet.** For local use:

```powershell
# Python 3.12 recommended (match the planned deployment runtime)
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Linux/macOS use `python3.12 -m venv .venv`, `source .venv/bin/activate`, then the same `pip install` and `streamlit run` commands. Run from the repository root. The app does not require an API key or a running LLM service.

For a test environment, additionally install `python -m pip install -r requirements-dev.txt`.

## What is implemented

| Section | Function | Boundary |
| --- | --- | --- |
| **Overview** | Investigation descriptions, record counts and quality-status summary | Counts are not confidence scores |
| **Explore** | FLEX source-linked record filters, Plotly charts, QC details; BASS-II Table 2.1 Evidence Card | Sources describe physically different fuels and observables |
| **Search** | Deterministic, explainable keyword retrieval and lexical ranking for the audited FLEX sample | Rank is not reliability or verified scientific truth |
| **Verify** | FLEX structured NASA-EVP checks and constrained English Table IX claim parsing; separate BASS-II source-cell verifier | No free-form scientific reasoning or causal prediction |
| **Evidence Ledger** | Separate session records and JSON exports for observed FLEX and BASS-II checks | Session-scoped, not a permanent audit server |
| **Methods & Limitations** | Source provenance, quality restrictions and prohibited interpretations | Important scientific exclusions remain in effect |

English is the default UI; Russian is optional. The English claim parser supports only narrow source-transcription templates. Russian-language scientific claim parsing is **not supported**. Original NASA identifiers, units, source locators, QC codes and machine-readable JSON fields remain unchanged in both UI languages.

## Audited source coverage

**FLEX — liquid fuel droplets (NASA/TP-2015-216046, PSI-69).** A small versioned D7 sample from Table IX: **17 source-linked records**, of which **10** have D4 `VERIFIED` status for limited source-point lookup and **7** have D4 `REVIEW` status. The sample is **not** the full FLEX experiment corpus. Literal missing marks, source conflicts and anomalous raw values are preserved; flagged fields are blocked from physical use. Report counts (284 reported tests, 276 earlier audited table rows and 275 earlier PSI entries) refer to potentially different entities and have not been fully reconciled.

**BASS-II — solid-fuel combustion (NASA/TM-20210011385, PSI-25).** An independent D7 release from **Table 2.1**, printed page 28 / PDF page 36: **two oxygen-condition rows** and **six method-specific evidence cells** (2 experimental, 2 computational, 2 theoretical), **not six independent experiments**. It reports 21% O₂: experiment **10±5**, computation **15**, theory **7.5 mm/s**; 16% O₂: experiment **30±5**, computation **35**, theory **10 mm/s**. The experimental uncertainty is reported; the model uncertainties are **not reported**, not zero. The unresolved Table 2.1 / Section 2.2.5 discrepancy and unproven as-run test ID mapping are explicitly retained.

These studies are kept separate; FLEX droplet metrics are not pooled quantitatively with BASS-II solid-fuel metrics. Details, source rights, and exact references are in [SOURCES.md](SOURCES.md).

## A reproducible demonstration

1. Open **Explore**, find `FLEX-002`, and inspect the raw oxygen mole fraction and NASA Table IX source anchor.
2. Open **Search** and find `FLEX-034`; inspect the conflict between the reported extinction-diameter cell and Figure 38. D4 `REVIEW` does not mean zero or a validated physical measurement.
3. In **Verify → FLEX**, evaluate a correctly attributed Table IX oxygen claim (for example, `0.21` for FLEX-002) and a conflicting value (`0.34`). Inspect the observed NASA-EVP verdict and evidence checks.
4. In **Explore**, inspect BASS-II at 21% and 16% nominal O₂. Compare the **published method columns** without combining them into experiments.
5. In **Verify → BASS-II**, verify `10±5 mm/s` for 21% O₂ / `EXPERIMENTAL` and compare with the incomplete assertion `10 mm/s` (without the reported ±5).
6. Open **Evidence Ledger**, inspect the separate ledgers and export JSON. A page refresh/new session may remove session-only history.

**Important:** D4 data quality `VERIFIED` is *not* the NASA-EVP scientific verdict `SUPPORTED`. A technical `ERROR` is not a scientific verdict.

## Validation

The latest archived build was independently rerun with the following results:

```text
python -m pytest -q                  # 206 passed
python -m benchmarks.run_r4_benchmark
                                       # FLEX 18/18 PASS
python -m benchmarks.run_bassii_benchmark
                                       # BASS-II 10/10 PASS
```

The two D7 integrity validators also passed. These tests evaluate bounded registered cases; they do not prove general scientific correctness or constitute a public-browser deployment test.

For the full release and deployment checklist see [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md) and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Scientific boundaries

VERGE does **not** simulate spacecraft fires, certify flame-suppression systems, predict safe ventilation thresholds, rank physical fire hazards, or extrapolate ISS microgravity observations to lunar/Martian partial gravity. Raw reported values can be transcribed with their restrictions without establishing physical validity. Source-based warnings and missing values must not be suppressed or silently corrected.

## Attribution, licensing and AI assistance

NASA publications and PSI records are attributed with report identifiers, investigation IDs, page/table locators and public source URLs. NASA reports and linked media retain their individual rights and attribution requirements; the project's Apache-2.0 license does not relicense NASA documents. No original heavyweight NASA PDF is required in this repository.

The software was produced by **one human participant** with **OpenAI ChatGPT (GPT-6) used for research, planning, drafting, debugging and test assistance**. The human developer reviewed and executed the code and its local tests. **No OpenAI model or other external LLM is currently invoked at runtime.** See [docs/AI_DISCLOSURE.md](docs/AI_DISCLOSURE.md) and [docs/R0_COMPLIANCE.md](docs/R0_COMPLIANCE.md).

## License

Original project code and documentation: [Apache License 2.0](LICENSE), where the author holds the relevant rights. NASA and third-party data, reports, images and software retain their own terms. VERGE is independent from NASA and is not NASA-endorsed.
