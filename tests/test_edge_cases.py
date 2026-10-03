"""Public-safe data-quality boundaries and mocked external validation."""

import pandas as pd
import pytest
import requests

from src.formatter import normalize_email, normalize_text
from src.pipeline import load_input, run_pipeline
from src.places_validator import GooglePlacesValidator


def process(tmp_path, rows, **kwargs):
    source = tmp_path / "input.csv"
    pd.DataFrame(rows, columns=["name", "address", "phone", "email", "specialty", "state"]).to_csv(
        source, index=False
    )
    return run_pipeline(
        source, tmp_path / "output.csv", "cardiology", "OH", GooglePlacesValidator(), **kwargs
    )


def row(**changes):
    return (
        dict(
            name="Example Cardiology",
            address="1 Example St",
            phone="2165550102",
            email="CONTACT@EXAMPLE.COM",
            specialty="cardiology",
            state="OH",
        )
        | changes
    )


@pytest.mark.parametrize("rows", [[], [row(state="IL")]])
def test_empty_population_keeps_output_contract(tmp_path, rows):
    result = process(tmp_path, rows)
    assert result.empty and len(result.columns) == 9
    assert pd.read_csv(tmp_path / "output.csv").empty


def test_missing_names_removed_missing_contacts_flagged_and_deduplicated(tmp_path):
    base = row()
    rows = [
        base,
        base.copy(),
        {**base, "name": None},
        {**base, "name": "Unknown"},
        {**base, "name": "Other Example", "phone": None, "email": None},
    ]
    result = process(tmp_path, rows)
    assert list(result["name"]) == ["Example Cardiology", "Other Example"]
    assert result.iloc[0]["email"] == "contact@example.com"
    assert result.iloc[1]["anomaly_flag"] == "invalid_phone;invalid_email"
    assert normalize_text(float("nan")) == normalize_email(float("nan")) == ""


@pytest.mark.parametrize("specialty,state", [("unsupported", "OH"), ("cardiology", "XX")])
def test_unknown_configuration_target_rejected(tmp_path, specialty, state):
    with pytest.raises(ValueError, match="Target specialty/state"):
        run_pipeline(tmp_path / "missing.csv", tmp_path / "out.csv", specialty, state)


def test_missing_columns_and_unsupported_format(tmp_path):
    source = tmp_path / "missing.csv"
    source.write_text("name\nExample\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Missing required columns"):
        run_pipeline(source, tmp_path / "out.csv", "cardiology", "OH")
    with pytest.raises(ValueError, match="Unsupported input format"):
        load_input(tmp_path / "legacy.xls")


def test_xlsx_input(tmp_path):
    source = tmp_path / "public.xlsx"
    pd.DataFrame([row()]).to_excel(source, index=False)
    result = run_pipeline(source, tmp_path / "out.csv", "cardiology", "OH", GooglePlacesValidator())
    assert len(result) == 1


@pytest.mark.parametrize(
    "status,results,valid",
    [("OK", [{}], True), ("ZERO_RESULTS", [], False), ("REQUEST_DENIED", [], False)],
)
def test_places_response_boundaries(monkeypatch, status, results, valid):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return {"status": status, "results": results}

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: Response())
    assert GooglePlacesValidator("dummy-key").validate("Example", "Public address").valid is valid


def test_places_transport_error_does_not_expose_key(monkeypatch):
    def fail(*args, **kwargs):
        raise requests.HTTPError("https://example.invalid/?key=dummy-private-key")

    monkeypatch.setattr(requests, "get", fail)
    with pytest.raises(RuntimeError, match="Google Places validation request failed") as error:
        GooglePlacesValidator("dummy-private-key").validate("Example", "Public address")
    assert "dummy-private-key" not in str(error.value)
    assert error.value.__suppress_context__
