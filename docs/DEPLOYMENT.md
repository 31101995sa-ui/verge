# VERGE — Public deployment and local Gemini operation

**Document updated:** 15 November 2026.
**Observed published baseline:** GitHub `main` at [`d041cbe`](https://github.com/31101995sa-ui/verge/commit/d041cbec3d097d648b8f3970e1356120194c3dfb), app at https://verge-microgravity.streamlit.app/.
**Public capability:** deterministic Streamlit dashboard; **Gemini execution is gated to trusted localhost**.

## 1. Reproducing the public baseline

The web app uses Python 3.12, `app.py` as entrypoint, `.streamlit/config.toml`, and runtime packages pinned in `requirements.txt` (Streamlit/pandas/Plotly). The GitHub repository includes both D7 releases; original heavyweight NASA PDFs are not required at runtime.

From PowerShell on Windows:

```powershell
# In a new location, for reproducibility rather than changing the working repo:
git clone https://github.com/31101995sa-ui/verge.git
cd verge
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
python data/releases/FLEX-R1-SAMPLE-20261114-v1.0/FLEX_R1_D7_validation_check.py
python data/releases/BASSII-R5-TABLE2_1-20261114-v1.0/BASS_II_R5_D7_validation_check_v1.py
python -m benchmarks.run_r4_benchmark --output "$env:TEMP\verge_flex_observed.json"
python -m benchmarks.run_bassii_benchmark --output "$env:TEMP\verge_bassii_observed.json"
python -m streamlit run app.py
```

These are reproducibility commands. The participant previously observed **237 passed** and **18/18 + 10/10** before publication of R6; a **fresh clean-clone full-suite rerun after `d041cbe` remains to be observed**. Both active D7 validators also passed independently in the reviewed archive. Do not label an unexecuted cloud-side test as PASS.

`data/releases/*/*` and `data/audit/*` are byte-preserved by `.gitattributes` (`-text`). Do not normalize CRLF/LF in these source-locked files, edit D7 manifests to match altered payloads, or change frozen benchmark expectations.

## 2. Current Streamlit Cloud deployment

- **Repository:** https://github.com/31101995sa-ui/verge
- **Branch:** `main`
- **Entry:** `app.py`
- **Runtime dependencies:** `requirements.txt`
- **Public URL:** https://verge-microgravity.streamlit.app/
- **Gemini:** no public credential is provisioned; manual local-only gate prevents rendering its UI on the cloud deployment with non-loopback bind address.

After any docs-only commit, Streamlit Cloud may redeploy; inspect build status and perform a quick public smoke test in a private browser. New public users must not be required to enter a Gemini API key. The app may take time to wake from host inactivity; a loading delay alone is not proof of broken code.

## 3. Local-only live Gemini demonstration

Run only from a trusted local development environment:

```powershell
python -m pip install -r requirements-gemini.txt
$env:VERGE_ENABLE_GEMINI_LOCAL = "1"
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8527
```

Open `http://127.0.0.1:8527` → Search → AI Evidence Interpretation. Select one study and 1–4 snippets. Enter a **personal Gemini API key locally** in the password field. The key is needed for each manually initiated provider call; it is **not** read from public Streamlit secrets. This local form is not an audited secure BYOK gateway. Do not live-share the password field, store keys in checked-in files, or claim complete post-call erasure. `google-genai==3.3.0` is an optional SDK pinned only by `requirements-gemini.txt`.

The draft must show `CANDIDATE_NOT_VERIFIED` and exact source identifiers. If the API refuses/limits a request, the deterministic dashboard remains the primary fallback; do not conceal blocked responses or treat them as scientific failures.

## 4. Final public browser smoke checklist

1. Open the live URL in a private browser with no credentials; verify Overview counts **17 FLEX** (10 VERIFIED / 7 REVIEW) and **6 BASS-II method cells**.
2. Navigate six main tabs; change English/Russian display and confirm identifiers and units remain unchanged.
3. Search `FLEX-034`; inspect the `REVIEW` and figure/table discrepancy, not a safety judgement.
4. Verify FLEX-002 oxygen mole fraction **0.21** (`SUPPORTED` source transcription) and deliberately false **0.99** (`CONTRADICTED`), and inspect printed p.20 / PDF p.26 Table IX locator.
5. Verify BASS-II experimental **10±5 mm/s** for 21% O₂; inspect Table 2.1 printed p.28 / PDF p.36 and uncertainty distinction.
6. Open both Evidence Ledgers and inspect the session-only warning and JSON download controls.
7. Ensure Gemini live input is **not visible on public Streamlit**; no public API key is needed.
8. Recheck that the public `main` repository includes all three `src/gemini_*.py` files and optional dependency file, although live execution remains local only.

The R8 independent reviewer already observed several public deterministic scenarios before R6 publication; repeating them now documents the latest deployed version.

## 5. Deployment and submission boundaries

The public app is not a guaranteed always-on service; keep the real slide screenshots/recording as presentation fallback. The **Project** page on the official Space Apps team site must be submitted separately before the applicable deadline; a GitHub/Streamlit URL is not an official submission receipt. Do not infer that a challenge-specific NASA Resources requirement is satisfied from NTRS/PSI links alone.

## References

- [Streamlit Community Cloud deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Streamlit app dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
- [2026 NASA Space Apps Challenge](https://www.spaceappschallenge.org/2026/)
- [Challenge Resources](https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/?tab=resources)
