# Architecture

The public repository implements a sanitized version of a healthcare lead
processing pattern. It contains synthetic data only.

Flow:

CSV / XLSX
  -> load and normalize columns
  -> state whitelist
  -> specialty whitelist
  -> blacklist filtering
  -> optional Google Places validation
  -> name + phone deduplication
  -> phone and email normalization
  -> placeholder removal
  -> anomaly flags
  -> sorted CSV output

## Design principles

- Configuration is separated from pipeline logic.
- External validation has a no-key fallback for local testing.
- The test suite uses only synthetic sample data.
- Credentials belong in environment variables and are excluded by .gitignore.
- The public repository contains no real provider or patient data.
