# VERGE — Release Candidate Checklist

**Release state:** not yet frozen. Complete and record real outputs before making acceptance claims.

## Code and data integrity

- [ ] Current Git HEAD documented; reviewed files committed, unrelated historical audits excluded deliberately.
- [ ] `python -m pytest -q` PASS (archived baseline **206/206**).
- [ ] FLEX case benchmark PASS (**18/18**).
- [ ] BASS-II case benchmark PASS (**10/10**).
- [ ] Standalone FLEX and BASS-II D7 validators PASS.
- [ ] Neither released raw/curated/QC source CSV nor D7 manifest changed unexpectedly.
- [ ] `.gitattributes` preserves exact release bytes; **a clean clone of the new Git commit passes both standalone D7 validators and the full Pytest suite**.
- [ ] D4 source-data QC status and NASA-EVP scientific verdict remain distinct; technical `ERROR` not a scientific verdict.
- [ ] No pooled physical comparisons between FLEX droplet data and BASS-II solid-fuel data.

## User experience and traceability

- [ ] Six navigation tabs load in EN and RU.
- [ ] Explorer and Search retain selections through language switching.
- [ ] Source links, original units, `0` vs missing `–`, numerical uncertainties and QC restrictions are visible.
- [ ] FLEX-034 Figure 38 and BASS-II Table 2.1/Section 2.2.5 restrictions are shown.
- [ ] Both structured verification workflows work, including deliberately false claims.
- [ ] Separate Evidence Ledgers export machine-readable JSON; session limitation disclosed.

## Public delivery

- [ ] Minimal cloud dependencies resolved in a clean Python 3.12 installation.
- [ ] README, SOURCES, AI disclosure, license, `.gitignore`, PROJECT_STATE reviewed and committed.
- [ ] Git tracked files contain no secrets, personal scratch material, raw heavyweight NASA PDFs or unintended binaries.
- [ ] GitHub repo is accessible without authentication; source data release paths exist remotely.
- [ ] Public Streamlit URL loads in an incognito browser and passes [deployment smoke test](DEPLOYMENT.md).
- [ ] The actual public URL and Git commit hash recorded.

## Competition and evidence

- [ ] Directly confirm at least one **actually used** NASA source in 2026 *Flame in Freefall* official Resources; record its exact link.
- [ ] Report and PSI source attributions and third-party rights are reviewed.
- [ ] AI assistance disclosed; no unimplemented runtime LLM described as implemented.
- [ ] English project description and short demonstration are ready under the current submission rules.
- [ ] Local judging deadline and presentation requirements confirmed with organizer.
- [ ] Project page submitted before **2026-11-15 23:59 Asia/Almaty**, with receipt/screenshots.

**No item is complete merely because it is listed here.**
