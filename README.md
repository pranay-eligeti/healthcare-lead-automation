# 🏥 Healthcare Lead Automation System

> A sanitized, runnable portfolio implementation of a 14-step healthcare lead-data cleaning pattern using Python and configuration-driven validation.

[![Python CI](https://github.com/pranay-eligeti/healthcare-lead-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/pranay-eligeti/healthcare-lead-automation/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-data%20processing-green)
![pytest](https://img.shields.io/badge/tests-pytest-orange)

## What this repository is

This repository is a **public portfolio adaptation** of a healthcare lead-processing architecture I have used in professional automation work.

It is deliberately sanitized. The repository contains **synthetic sample data only** and no PHI, employer exports, credentials, internal URLs, or proprietary source code.

The implementation demonstrates the engineering pattern:

- deterministic filtering
- configuration-driven specialty/state rules
- blacklist protection
- optional external validation
- deduplication
- contact normalization
- anomaly flags
- reproducible CSV output
- automated tests and GitHub Actions CI

## Pipeline

    Input CSV / XLSX
          |
          v
    1. Load
          |
    2. Normalize columns
          |
    3. Drop empty rows
          |
    4. State whitelist
          |
    5. Specialty whitelist
          |
    6. Blacklist filtering
          |
    7. Optional Places validation
          |
    8. Name + phone deduplication
          |
    9. Phone normalization
          |
   10. Email normalization/validation
          |
   11. Placeholder removal
          |
   12. Anomaly flags
          |
   13. Sort/structure
          |
   14. Export CSV

The configuration shipped with the repository models **14 specialties** and **4 states** from the broader workflow pattern.

## Repository structure

    healthcare-lead-automation/
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    ├── config/
    │   ├── blacklist.json
    │   ├── specialties.json
    │   └── states.json
    ├── docs/
    │   └── architecture.md
    ├── sample_data/
    │   └── leads.csv
    ├── src/
    │   ├── __init__.py
    │   ├── exporter.py
    │   ├── filters.py
    │   ├── formatter.py
    │   ├── pipeline.py
    │   └── places_validator.py
    ├── tests/
    │   └── test_pipeline.py
    ├── .env.example
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt

## Quick start

### 1. Clone

    git clone https://github.com/pranay-eligeti/healthcare-lead-automation.git
    cd healthcare-lead-automation

### 2. Install

    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate

    pip install -r requirements.txt

### 3. Run the sample

    python -m src.pipeline \
      --input sample_data/leads.csv \
      --specialty "cardiology" \
      --state "OH" \
      --output output/cardiology_oh.csv

With no Google Places API key, external validation is skipped so the sample can run locally without credentials.

### 4. Run tests

    pytest -q

## Engineering notes

**Configuration over hard-coding**  
Specialty keywords, state aliases, and blacklist patterns live under `config/`.

**Safe external dependency**  
Google Places validation is optional. Local/test runs do not require an API key.

**Data-quality controls**  
Phone normalization, email validation, duplicate protection, placeholder removal, and anomaly flags are explicit pipeline stages.

**Reproducibility**  
The project includes sample data, dependency bounds, tests, and GitHub Actions CI.

## Security and privacy

Never commit:

- real healthcare records
- patient/provider exports containing sensitive information
- API keys or passwords
- employer-only workflows or internal URLs

Use `.env` for secrets and keep real operational data outside this public repository.

## Connection to my professional work

My professional healthcare automation work includes provider-data acquisition, multi-step cleaning and standardization, data-quality controls, and workflow orchestration. This repository is the **public, sanitized implementation used to demonstrate those engineering patterns** without exposing private business systems.

## License

MIT
