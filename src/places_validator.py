"""Optional Google Places validation with a safe no-key fallback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

@dataclass(frozen=True)
class PlacesValidationResult:
    valid: bool
    reason: str

class GooglePlacesValidator:
    def __init__(self, api_key: str | None = None, timeout: int = 10) -> None:
        self.api_key = api_key
        self.timeout = timeout

    def validate(self, name: str, address: str) -> PlacesValidationResult:
        if not self.api_key:
            return PlacesValidationResult(True, "skipped:no_api_key")

        response = requests.get(
            "https://maps.googleapis.com/maps/api/place/textsearch/json",
            params={"query": f"{name} {address}".strip(), "key": self.api_key},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        status = payload.get("status")
        if status not in {"OK", "ZERO_RESULTS"}:
            return PlacesValidationResult(False, f"places_status:{status}")

        return (
            PlacesValidationResult(True, "match_found")
            if payload.get("results")
            else PlacesValidationResult(False, "no_match")
        )
