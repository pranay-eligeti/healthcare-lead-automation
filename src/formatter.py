"""Formatting and lightweight validation helpers."""

from __future__ import annotations

import re
from typing import Any

PLACEHOLDER_VALUES = {
    "", "n/a", "na", "none", "null", "unknown", "test", "placeholder"
}

def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())

def normalize_phone(value: Any) -> str:
    text = re.sub(r"\D+", "", normalize_text(value))
    if len(text) == 11 and text.startswith("1"):
        text = text[1:]
    if len(text) != 10:
        return ""
    return f"({text[:3]}) {text[3:6]}-{text[6:]}"

def normalize_email(value: Any) -> str:
    return normalize_text(value).lower()

def is_valid_email(value: Any) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalize_email(value)))

def is_placeholder(value: Any) -> bool:
    return normalize_text(value).lower() in PLACEHOLDER_VALUES
