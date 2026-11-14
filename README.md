
# VERGE-NASA Edition

**Stellar Anvil | NASA Space Apps Challenge 2026**

Challenge: Flame in Freefall — Microgravity Combustion Research

## Mission

VERGE-NASA Edition is an evidence-centered scientific research dashboard designed to make NASA microgravity combustion experiments easier to search, examine, compare, and interpret.

The intended workflow is:

SEARCH → SUMMARIZE → RANK → INTERPRET → VERIFY → CRITIQUE

## Scientific Scope

The initial research scope includes:

- FLEX: Liquid-fuel droplet combustion and flame extinction.
- BASS-II: Solid-material combustion and flame spread.

These experiments represent different physical systems. Their numerical results must not be combined without scientifically justified comparability.

## Planned Capabilities

- Interactive experiment explorer
- Source-linked experimental records
- Transparent evidence relevance ranking
- Scientific interpretation with stated limitations
- Independent claim verification
- Reproducible evaluation and audit records

## Current Implementation Status

R0 — Initial application bootstrap.

Implemented:
- Python virtual environment
- Initial Streamlit interface
- Dependency configuration

Not yet implemented:
- NASA dataset ingestion
- Experimental data visualization
- Search and ranking
- Scientific claim verification
- AI-assisted interpretation

## Technology

- Python 3.12
- Streamlit
- Pandas
- PyMuPDF
- Plotly
- Pytest

## Local Setup

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Launch the application:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Scientific Integrity

Experimental statements must be traceable to NASA sources.

The system distinguishes measured values, derived values, reported findings, interpretations, and unknown information.

A language model cannot independently certify its own scientific claims.

Unsupported predictions and extrapolations beyond the investigated conditions are not presented as verified findings.

## Limitations

This project is not a validated spacecraft fire simulator, an operational fire suppression controller, or a safety certification system.

Results from ISS microgravity experiments must not be directly generalized to lunar or Martian gravity.

## Sources

See [SOURCES.md](SOURCES.md).

## Development State

See [PROJECT_STATE.md](docs/PROJECT_STATE.md).

## AI Assistance

ChatGPT is used as an AI development and research assistant. The project has one human participant, responsible for final decisions, testing, verification, and submission.

## License


## License

Original project code is licensed under Apache-2.0.
See [LICENSE](LICENSE).

NASA datasets, publications, imagery, and third-party
dependencies retain their respective licenses and
usage conditions.

This is an independent project developed for the
NASA Space Apps Challenge 2026. It is not an
official NASA product or NASA-endorsed software.

