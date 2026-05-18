from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import RAW_DATA_DIR, SAMPLE_DATA_DIR


def _load_csv(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {label} at {path}. "
            "Run `python scripts/generate_synthetic_data.py` for the public demo, "
            "or provide a local restricted-data path explicitly."
        )
    return pd.read_csv(path)


def _resolve_path(
    sample_path: Path,
    raw_path: Path,
    label: str,
    sample: bool = True,
    path: str | Path | None = None,
) -> pd.DataFrame:
    if path is not None:
        return _load_csv(Path(path), label)
    if sample:
        return _load_csv(sample_path, label)
    if raw_path.exists():
        return _load_csv(raw_path, label)
    raise FileNotFoundError(
        f"No restricted {label} file was found at {raw_path}. "
        "Pass an explicit path or load the synthetic sample instead."
    )


def load_encounters(sample: bool = True, path: str | Path | None = None) -> pd.DataFrame:
    df = _resolve_path(
        SAMPLE_DATA_DIR / "synthetic_encounters.csv",
        RAW_DATA_DIR / "encounters.csv",
        "encounters data",
        sample=sample,
        path=path,
    )
    if "county_fips" in df.columns:
        df["county_fips"] = (
            df["county_fips"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(5)
        )
    return df


def load_county_panel(sample: bool = True, path: str | Path | None = None) -> pd.DataFrame:
    df = _resolve_path(
        SAMPLE_DATA_DIR / "synthetic_county_panel.csv",
        RAW_DATA_DIR / "county_panel.csv",
        "county panel data",
        sample=sample,
        path=path,
    )
    if "county_fips" in df.columns:
        df["county_fips"] = (
            df["county_fips"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(5)
        )
    return df


def load_campus_scores(sample: bool = True, path: str | Path | None = None) -> pd.DataFrame:
    df = _resolve_path(
        SAMPLE_DATA_DIR / "synthetic_campus_scores.csv",
        RAW_DATA_DIR / "campus_scores.csv",
        "campus scoring data",
        sample=sample,
        path=path,
    )
    if "county_fips" in df.columns:
        df["county_fips"] = (
            df["county_fips"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(5)
        )
    return df
