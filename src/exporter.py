"""Output helpers."""

from __future__ import annotations

from pathlib import Path
import pandas as pd

def write_csv(df: pd.DataFrame, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path
