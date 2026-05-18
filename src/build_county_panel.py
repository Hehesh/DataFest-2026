from __future__ import annotations

import numpy as np
import pandas as pd

from .clean_encounters import filter_diabetes_patients


def compute_diabetes_acute_care_rate(county_df: pd.DataFrame) -> pd.DataFrame:
    result = county_df.copy()
    result["diabetes_acute_care_rate"] = np.where(
        result["diabetes_patients"] > 0,
        result["acute_care_events"] / result["diabetes_patients"] * 100,
        np.nan,
    )
    return result


def build_county_panel(encounters: pd.DataFrame) -> pd.DataFrame:
    diabetes = filter_diabetes_patients(encounters)
    diabetes = diabetes[diabetes["county_fips"].notna() & (diabetes["county_fips"] != "")]
    diabetes = diabetes.copy()
    diabetes["acute_care_event"] = diabetes[
        ["is_ed", "is_hospital_admittance", "is_observation"]
    ].max(axis=1)

    county_panel = (
        diabetes.groupby(["county_fips", "county_name", "year"], as_index=False)
        .agg(
            diabetes_patients=("patient_id", "nunique"),
            acute_care_events=("acute_care_event", "sum"),
            average_distance_to_nearest_campus=("distance_to_nearest_campus_miles", "mean"),
        )
    )

    county_panel["acute_care_events"] = county_panel["acute_care_events"].astype(int)
    return compute_diabetes_acute_care_rate(county_panel)
