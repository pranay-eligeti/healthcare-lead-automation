"""Config-driven filtering for states, specialties, and known bad entries."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

from .formatter import normalize_text

def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def matches_state(value: object, state: str, state_config: dict[str, list[str]]) -> bool:
    target = normalize_text(state).upper()
    raw = normalize_text(value).upper()
    aliases = {target, *[x.upper() for x in state_config.get(target, [])]}
    return raw in aliases

def matches_specialty(value: object, specialty: str, specialty_config: dict[str, list[str]]) -> bool:
    target = normalize_text(specialty).lower()
    raw = normalize_text(value).lower()
    return any(re.search(re.escape(keyword.lower()), raw) for keyword in specialty_config.get(target, []))

def contains_blacklisted(value: object, patterns: Iterable[str]) -> bool:
    text = normalize_text(value).lower()
    return any(re.search(pattern.lower(), text) for pattern in patterns)
