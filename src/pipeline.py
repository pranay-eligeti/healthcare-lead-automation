"""End-to-end healthcare lead cleaning pipeline.

This public version is intentionally sanitized: it uses synthetic data and
contains no employer data, PHI, credentials, or proprietary code.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from .exporter import write_csv
from .filters import contains_blacklisted, load_json, matches_specialty, matches_state
from .formatter import (
    is_placeholder,
    is_valid_email,
    normalize_email,
    normalize_phone,
    normalize_text,
)
from .places_validator import GooglePlacesValidator

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"


def load_input(path: str | Path) -> pd.DataFrame:
    source = Path(path)
    if source.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(source)
    if source.suffix.lower() == ".csv":
        return pd.read_csv(source)
    raise ValueError(f"Unsupported input format: {source.suffix}")


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {
        column: normalize_text(column).lower().replace(" ", "_")
        for column in df.columns
    }
    return df.rename(columns=renamed)


def run_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    specialty: str,
    state: str,
    places_validator: GooglePlacesValidator | None = None,
) -> pd.DataFrame:
    specialties = load_json(CONFIG_DIR / "specialties.json")
    states = load_json(CONFIG_DIR / "states.json")
    blacklist = load_json(CONFIG_DIR / "blacklist.json")["name_patterns"]

    # 1. Load
    df = load_input(input_path)

    # 2. Normalize columns
    df = clean_columns(df)

    required = {"name", "address", "phone", "email", "specialty", "state"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # 3. Drop empty rows
    df = df.dropna(how="all").copy()

    # 4. State whitelist
    df = df[df["state"].apply(lambda value: matches_state(value, state, states))].copy()

    # 5. Specialty whitelist
    df = df[
        df["specialty"].apply(
            lambda value: matches_specialty(value, specialty, specialties)
        )
    ].copy()

    # 6. Blacklist filtering
    df = df[
        ~df["name"].apply(lambda value: contains_blacklisted(value, blacklist))
    ].copy()

    # 7. Optional external validation
    validator = places_validator or GooglePlacesValidator(
        os.getenv("GOOGLE_PLACES_API_KEY")
    )
    validation = df.apply(
        lambda row: validator.validate(
            normalize_text(row["name"]),
            normalize_text(row["address"]),
        ),
        axis=1,
    )
    df["places_validation"] = [item.reason for item in validation]
    validation_mask = validation.map(lambda item: item.valid)
    df = df.loc[validation_mask].copy()

    # 8. Deduplicate by phone + normalized name
    df["_dedupe_name"] = df["name"].apply(normalize_text).str.lower()
    df["_dedupe_phone"] = df["phone"].apply(normalize_phone)
    df = df.drop_duplicates(
        subset=["_dedupe_name", "_dedupe_phone"], keep="first"
    ).copy()

    # 9. Phone formatting
    df["phone"] = df["phone"].apply(normalize_phone)

    # 10. Email normalization and validation
    df["email"] = df["email"].apply(normalize_email)
    df["email_valid"] = df["email"].apply(is_valid_email)

    # 11. Remove placeholder rows
    df = df[~df["name"].apply(is_placeholder)].copy()

    # 12. Flag remaining anomalies
    df["anomaly_flag"] = ""
    df.loc[df["phone"].eq(""), "anomaly_flag"] = "invalid_phone"
    invalid_email = ~df["email_valid"]
    df.loc[invalid_email, "anomaly_flag"] = df.loc[
        invalid_email, "anomaly_flag"
    ].map(lambda value: f"{value};invalid_email".strip(";"))

    # 13. Sort and structure output
    output_columns = [
        "name",
        "address",
        "phone",
        "email",
        "specialty",
        "state",
        "places_validation",
        "email_valid",
        "anomaly_flag",
    ]
    result = (
        df[output_columns]
        .sort_values(["state", "specialty", "name"])
        .reset_index(drop=True)
    )

    # 14. Export
    write_csv(result, output_path)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean and validate healthcare lead data."
    )
    parser.add_argument("--input", required=True, help="CSV or XLSX input")
    parser.add_argument("--specialty", required=True, help="Target specialty")
    parser.add_argument("--state", required=True, help="Target US state code")
    parser.add_argument("--output", required=True, help="CSV output path")
    return parser


def main() -> None:
    load_dotenv(ROOT / ".env")
    args = build_parser().parse_args()
    result = run_pipeline(args.input, args.output, args.specialty, args.state)
    print(f"Processed {len(result)} records -> {args.output}")


if __name__ == "__main__":
    main()
