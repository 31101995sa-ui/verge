# Deploy VERGE — NASA Edition (Streamlit Community Cloud)

**Status:** deployment procedure prepared; a real public deployment is **not yet verified**.

## 1. Freeze the local state

From the project root on Windows PowerShell:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m benchmarks.run_r4_benchmark --output artifacts/r4_benchmark_v0.1.json
python -m benchmarks.run_bassii_benchmark --output artifacts/r5_bassii_benchmark_v0.1.json
python .\data\releases\FLEX-R1-SAMPLE-20261114-v1.0\FLEX_R1_D7_validation_check.py
python .\data\releases\BASSII-R5-TABLE2_1-20261114-v1.0\BASS_II_R5_D7_validation_check_v1.py
git status --short --untracked-files=all
```

`requirements.txt` is for the web runtime (Streamlit, Pandas and Plotly). `requirements-dev.txt` installs it plus Pytest for the test environment. The standalone D7 validators rely on standard Python libraries and the checked release files. The original NASA PDFs and heavy offline parsing tools are not required at web runtime.

The archived developer environment and the proposed deployment file may have different transitive packages. **A truly clean Python 3.12 installation is still required to confirm dependency resolution.**

**Critical Phase B.2 Git fix:** the archived `906e1ca` commit normalized the original CRLF bytes of two BASS-II CSVs, breaking the D7 manifest in a clean Git clone, despite passing in the developer working tree. The release package includes `.gitattributes` with `-text` for `data/releases/*/*` and `data/audit/*`. Before deployment stage the four unchanged canonical source CSV bytes listed in `INSTALL_M2.md` under these attributes; do not edit their contents. A **fresh Git clone must pass both D7 validators** before publication.

## 2. Publish reviewed Git files only

Before publication, inspect staged paths (`git diff --cached --name-only`) and tracked files (`git ls-files`). Exclude `.env`, `.streamlit/secrets.toml`, virtual environments, raw NASA PDF sources, accidental local console files and any personal data. Verify `git log --format=fuller -3` if exposing a personal Git commit email is a concern.

Commit the deployment-readiness files and the four byte-preserved canonical scientific blobs separately from the tested R5/UI checkpoint. **First perform a clean-clone reproducibility test of that new commit.** Create a GitHub repository under an account you control, then connect the local checkout using the remote URL **actually provided by GitHub**. Do not publish or guess the remote URL before creating the repo.

```powershell
# Example placeholders only — replace with the actual GitHub URL.
git remote add origin <ACTUAL_GITHUB_REPOSITORY_URL>
git push -u origin main
```

The remote command is an example, not something to run before the repository exists. If `origin` already exists, inspect `git remote -v` instead of adding another remote.

## 3. Create the public Streamlit app

1. Sign in to https://share.streamlit.io/ using GitHub.
2. Click **Create app** and choose the actual published repository.
3. Branch: `main`; entrypoint: **`app.py`**.
4. In **Advanced settings**, choose **Python 3.12** to match the intended runtime. Streamlit Cloud's default may change.
5. Use the root `requirements.txt` and checked `.streamlit/config.toml`. No secrets need to be configured for the current deterministic app.
6. Deploy, read the real build logs, and copy the **actual** `*.streamlit.app` URL only after it loads.

Source paths are rooted at `Path(__file__).resolve().parent` in the app, so the two versioned D7 release folders must be included in the committed repository unchanged. Do not use absolute Windows paths in the cloud.

## 4. Public smoke test (fresh session)

Open the public URL in a new private/incognito browser, without developer credentials. Confirm:

1. Overview shows FLEX **17** records (10 `VERIFIED`, 7 `REVIEW`), and BASS-II **6** method cells (not independent experiments).
2. English is the default. Switching to Russian does not reset the chosen experiment or search text.
3. Explore can select **FLEX-002**, display original raw oxygen data and NASA locator.
4. Explore warns on **FLEX-034** and its figure conflict; a blocked datum is not treated as a reliable physical diameter.
5. Search finds source-linked records and shows that lexical relevance is not a scientific verdict.
6. Verify/FLEX accepts a supported bounded Table IX claim and rejects a deliberately incorrect numerical claim.
7. BASS-II Explore separates experiment, numerical computation and theory; model uncertainty is not reported.
8. Verify/BASS-II: 21% O₂ / experimental / **10±5 mm/s** is a literal source match; omitting the ±5 must not count as the same published cell.
9. Evidence Ledger shows separate FLEX and BASS-II histories and JSON download controls.
10. Methods & Limitations displays the unresolved Table 2.1 discrepancy and provenance links.
11. Refresh/fresh session does not reveal another visitor's session ledger. In-session results may be lost after a reload.

Treat failed cold startup, missing release files, broken links or missing QC notices as release blockers.

## 5. Deployment fallback

If cloud deployment fails and cannot be stabilized before release freeze, preserve the known-good local Streamlit server (`python -m streamlit run app.py`), take a short screen recording and screenshots, provide reproduction commands, and submit the required short demo/presentation. A Windows `.exe` is not required for this gate.

## References

- [Streamlit Community Cloud — deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [App dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
- [File organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)
- [NASA project submission guide](https://www.spaceappschallenge.org/resources/project-submission-guide/)
