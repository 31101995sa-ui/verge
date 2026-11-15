# VERGE — Verified Evidence and Risk-Governed Exploration

**Traceable evidence for microgravity combustion research**
Independent project for **NASA Space Apps Challenge 2026 — Flame in Freefall**
**Stellar Anvil · one human participant · AI-assisted development**

**Live dashboard:** https://verge-microgravity.streamlit.app/
**Source code:** https://github.com/31101995sa-ui/verge

VERGE is an English/Russian scientific evidence explorer. It links selected microgravity combustion observations to original NASA report locations, keeps data-quality warnings visible, and checks narrowly defined source claims using deterministic rules. A separate, **optional local-only Gemini extension** produces candidate interpretations based on selected records. Its prose is **not** independently verified as scientifically true.

Here, *risk-governed* means reducing unsupported source, unit, context, and scope claims. VERGE **does not calculate physical fire risk**, provide operational safety thresholds, or certify spacecraft systems. It is not an official NASA product, and NASA does not endorse it.

## Try VERGE — no installation

Open the [public dashboard](https://verge-microgravity.streamlit.app/) in a browser. The public version needs **no account, API key, or local Python installation**. It provides six main sections:

| Section | What is available | Important boundary |
| --- | --- | --- |
| **Overview** | FLEX/BASS-II coverage and data-quality counts | QC counts are not science-verdict accuracy |
| **Explore** | FLEX record filters, charts and raw provenance; BASS-II Table 2.1 card | Different fuel classes are not pooled |
| **Search** | Traceable lexical search and ranking of the 17-record FLEX sample | Ranking is relevance, not scientific confidence |
| **Verify** | Study-specific structured source-cell/scope checks and verdict explanations | No unrestricted natural-language proof or fire prediction |
| **Evidence Ledger** | Separate session histories and JSON download | Not persistent between browser sessions |
| **Methods & Limitations** | Source identities, audit restrictions and unresolved questions | Sources must be interpreted within their experimental scope |

**Public demo example:** in **Verify → FLEX**, select FLEX-002, the *oxygen mole fraction* source field and *dimensionless mole fraction* unit. `0.21` gives `SUPPORTED` for the specific source-cell transcription; a deliberately false `0.99` gives `CONTRADICTED`. The printed original is `.21` in NASA/TP-2015-216046, Table IX, printed p.20 / PDF p.26. The false value is a test input, **not** NASA data.

Another useful example is **Search → FLEX-034**, whose source table and figure caption are not fully reconciled; the interface retains its `REVIEW` status rather than treating it as an ordinary physical measurement.

## One-click Windows launch (prepared environment)

Windows users who already prepared the repository and its `.venv` can start the **full local dashboard** by double-clicking **[`Start_VERGE.cmd`](Start_VERGE.cmd)** in File Explorer. **VS Code and manual PowerShell commands are not required for daily use.** Keep the launcher beside `app.py` in the project root. The application should open in your default browser at **http://127.0.0.1:8527**.

**First-time setup (once per checkout):** this launcher is **not** a portable, self-contained EXE. It requires Python 3.12 and an existing project-local virtual environment with the dependencies installed. From the repository root, prepare them if needed:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-gemini.txt
```

`requirements-gemini.txt` installs the ordinary dashboard requirements plus the optional Google Gemini SDK. The launcher itself **never installs or upgrades packages**, never changes PowerShell execution policy, and never stores an API key.

**Using and closing the launcher:**

1. Double-click `Start_VERGE.cmd` in Windows Explorer. Leave its command window open while using VERGE. It starts Streamlit on **`127.0.0.1:8527` only** and enables the local Gemini panel in **Search → AI Evidence Interpretation**.
2. For a live Gemini draft, select FLEX or BASS-II evidence, enter your **own Google Gemini API key** in the local password field and submit a question; an Internet connection is required. No key is needed for the deterministic dashboard. Gemini text remains `CANDIDATE_NOT_VERIFIED`, never a scientific verdict.
3. Closing the **browser tab does not stop the server**. To reopen VERGE while the console window is still running, simply visit **http://127.0.0.1:8527**; do not double-click the launcher again.
4. To stop the server, return to the command window and press **Ctrl+C**. If Windows asks whether to terminate the batch job, confirm with **Y**. Once it exits, the launcher can be run again.

**Common diagnostics:** if the launcher reports **`Port 8527 is already in use`**, an existing local process is listening on that port; try the URL above if it is your VERGE server. Otherwise identify and stop your own server safely before retrying. The launcher **never kills another process**. If `.venv\Scripts\python.exe` or required libraries are missing, it displays an error instead of installing anything silently; install dependencies in that project's `.venv` first. Missing Gemini SDK or credentials must not block FLEX/BASS-II deterministic exploration and verification.

**Distribution boundary:** this is a one-click launcher **for an already prepared Windows machine**. A fresh computer still needs Python and dependency setup; no standalone portable package is claimed. The public [Streamlit dashboard](https://verge-microgravity.streamlit.app/) does **not** use this `.cmd` or expose the live Gemini form. See [deployment guidance](docs/DEPLOYMENT.md) for the manual launch and verification path.

## Actual scientific coverage

- **FLEX / PSI-69:** 17 selected liquid-fuel droplet records from NASA/TP-2015-216046, Table IX. D4 source-data review: **10 `VERIFIED` / 7 `REVIEW`**. This is a bounded sample, not the complete investigation.
- **BASS-II / PSI-25:** two oxygen-condition rows from NASA/TM-20210011385, Table 2.1 (printed p.28 / PDF p.36), represented as **six method-specific cells**: experimental, computational, analytical. These are **not six separate physical tests**; the unique as-run mapping is unresolved.

| Nominal oxygen | Reported experimental value (mm/s) | Computation (mm/s) | Theory (mm/s) |
| --- | ---: | ---: | ---: |
| 21% O₂ | 10 ± 5 | 15 | 7.5 |
| 16% O₂ | 30 ± 5 | 35 | 10 |

Model uncertainty is **not reported**, not zero. Differences between Table 2.1 and discussion in §2.2.5 remain unresolved. FLEX droplet observables must not be quantitatively combined with BASS-II solid-fuel findings. See [SOURCES.md](SOURCES.md) for precise attribution and known quality issues.

## Optional local Gemini candidate interpretation (R6)

For a prepared Windows setup, the recommended launch path is **[`Start_VERGE.cmd`](Start_VERGE.cmd)** as described above. The commands below are the **manual PowerShell alternative** (and also show how to prepare a new `.venv`).

The public code contains `src/gemini_candidate.py`, `src/gemini_evidence.py`, and `src/gemini_panel.py`. **Live Gemini is deliberately hidden from the public Streamlit deployment.** To use it on a trusted local computer:

```powershell
# Windows PowerShell, from the repository root; Python 3.12
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-gemini.txt
$env:VERGE_ENABLE_GEMINI_LOCAL = "1"
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8527
```

Open `http://127.0.0.1:8527` and visit **Search → AI Evidence Interpretation**. Choose **FLEX** or **BASS-II**; select **one to four** source snippets from **one study only**, ask a question in English or Russian, and enter **your own Gemini API key locally** in the password input. Never put a key in source code, Git, screenshots, or shared logs. The flag must be re-set in each new PowerShell process. Do **not** enter a personal key on an unfamiliar hosted replica.

The selected FLEX snippets exclude seven D4 `REVIEW` records. The Gemini result is always labelled `CANDIDATE_NOT_VERIFIED` with `CITATION_IDS_AND_FORMAT_ONLY`: output shape, known evidence IDs and a conservative digit restriction are checked. A single regeneration is allowed following a numeric-prose rejection. **The meaning of the generated prose is not independently verified**; valid citations do not prove an interpretation. Existing structured NASA-EVP checkers operate separately. An unavailable API does not remove the core deterministic dashboard.

No public API key is provisioned by the project. A local Gemini live smoke test with BASS-II was reported by the participant; the independent R8 audit checked adapter logic with mock clients rather than running a live provider call.

For basic public/local operation without Gemini, install `requirements.txt` instead and run `python -m streamlit run app.py`.

## Reproducible tests

From the repository root, install test dependencies with `python -m pip install -r requirements-dev.txt`. To run the optional Gemini tests without calling a provider, install `requirements-gemini.txt` as well, if needed for a local demo. Then run:

```powershell
python -m pytest -q
python data/releases/FLEX-R1-SAMPLE-20261114-v1.0/FLEX_R1_D7_validation_check.py
python data/releases/BASSII-R5-TABLE2_1-20261114-v1.0/BASS_II_R5_D7_validation_check_v1.py
python -m benchmarks.run_r4_benchmark --output "$env:TEMP\verge_flex_observed.json"
python -m benchmarks.run_bassii_benchmark --output "$env:TEMP\verge_bassii_observed.json"
```

**Observed on the participant's Windows environment before the R6 commit:** **237/237 Pytest PASS**, **18/18 FLEX benchmark**, **10/10 BASS-II benchmark**, and both D7 validators PASS. The published commit [`d041cbe`](https://github.com/31101995sa-ui/verge/commit/d041cbec3d097d648b8f3970e1356120194c3dfb) includes R6 and the byte-exact fix for two historical FLEX CSVs. The **post-commit fresh-clone full suite remains a separate acceptance check**; do not equate the preceding local run with all future environments passing. Benchmark results describe predefined claim cases, **not universal scientific accuracy**.

## Science and software boundaries

D4 `VERIFIED` describes a source-data QC step; it is **not** an NASA-EVP `SUPPORTED` verdict. `SUPPORTED`, `CONTRADICTED`, `INSUFFICIENT_EVIDENCE`, and `OUT_OF_SCOPE` apply only to supported structured obligations. A technical `ERROR` is not a scientific verdict. Source provenance is preserved without silently changing missing markers (`–`), literal zeros, unsupported conversions or flagged anomalies.

VERGE does **not** search all NASA publications, discover counterexamples autonomously, validate a physical fire model, predict Moon/Mars partial-gravity results, establish general safe ventilation settings, or certify fire safety. The optional Gemini draft does not close these gaps.

## Attribution, AI disclosure, licensing and challenge status

Sources: [SOURCES.md](SOURCES.md). AI assistance, including OpenAI ChatGPT development support and Google's local Gemini interpretation, is described in [docs/AI_DISCLOSURE.md](docs/AI_DISCLOSURE.md). Project-original code is licensed under [Apache-2.0](LICENSE); NASA reports and other third-party assets retain their respective rights. NASA is a credited research source and challenge organizer, **not** a product co-developer or endorser.

**Submission checks still open:** independently record a genuinely used source listed in the official [Flame in Freefall Resources](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/?tab=resources), confirm the applicable local event rules, and obtain a real submission receipt. The existence of this repository and live dashboard does not by itself mean the competition submission is complete. See [docs/R0_COMPLIANCE.md](docs/R0_COMPLIANCE.md), [docs/PROJECT_STATE.md](docs/PROJECT_STATE.md) and [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md).
