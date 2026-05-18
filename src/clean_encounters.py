from __future__ import annotations

import re

import pandas as pd

TRUTHY = {"1", "true", "t", "yes", "y"}


def _snake_case(name: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]+", "_", str(name).strip()).strip("_").lower()


def _to_binary(series: pd.Series) -> pd.Series:
    normalized = series.fillna(0).astype(str).str.strip().str.lower()
    return normalized.isin(TRUTHY).astype(int)


def clean_encounters(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [_snake_case(column) for column in cleaned.columns]

    required_columns = [
        "patient_id",
        "encounter_id",
        "county_fips",
        "county_name",
        "campus",
        "encounter_date",
        "is_diabetes",
        "is_ed",
        "is_hospital_admittance",
        "is_observation",
        "distance_to_nearest_campus_miles",
    ]
    missing = [column for column in required_columns if column not in cleaned.columns]
    if missing:
        raise KeyError(f"Encounter file is missing required columns: {missing}")

    cleaned["county_fips"] = (
        cleaned["county_fips"]
        .astype(str)
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(5)
    )
    cleaned["county_name"] = cleaned["county_name"].astype(str).str.strip()
    cleaned["campus"] = cleaned["campus"].astype(str).str.strip()
    cleaned["encounter_date"] = pd.to_datetime(cleaned["encounter_date"], errors="coerce")
    cleaned["distance_to_nearest_campus_miles"] = pd.to_numeric(
        cleaned["distance_to_nearest_campus_miles"],
        errors="coerce",
    )

    for column in ["is_diabetes", "is_ed", "is_hospital_admittance", "is_observation"]:
        cleaned[column] = _to_binary(cleaned[column])

    cleaned["year"] = cleaned["encounter_date"].dt.year
    return cleaned.dropna(subset=["encounter_date", "year"]).reset_index(drop=True)


def filter_diabetes_patients(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["is_diabetes"] == 1].copy()
