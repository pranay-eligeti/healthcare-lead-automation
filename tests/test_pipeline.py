from pathlib import Path

from src.pipeline import run_pipeline
from src.places_validator import GooglePlacesValidator

ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_filters_specialty_and_state(tmp_path):
    output = tmp_path / "out.csv"
    result = run_pipeline(
        ROOT / "sample_data" / "leads.csv",
        output,
        specialty="cardiology",
        state="OH",
        places_validator=GooglePlacesValidator(),
    )

    assert output.exists()
    assert list(result["name"]) == ["Lakeview Cardiology"]
    assert bool(result.iloc[0]["email_valid"]) is True


def test_pipeline_exports_expected_columns(tmp_path):
    output = tmp_path / "out.csv"
    result = run_pipeline(
        ROOT / "sample_data" / "leads.csv",
        output,
        specialty="cardiology",
        state="IL",
        places_validator=GooglePlacesValidator(),
    )

    expected = {
        "name",
        "address",
        "phone",
        "email",
        "specialty",
        "state",
        "places_validation",
        "email_valid",
        "anomaly_flag",
    }
    assert expected.issubset(result.columns)
