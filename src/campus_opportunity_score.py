from __future__ import annotations

import pandas as pd

from .access_need_score import normalize_series


def compute_campus_opportunity_score(
    df: pd.DataFrame,
    alpha: float = 1.0,
    beta: float = 1.0,
    delta: float = 0.5,
) -> pd.DataFrame:
    """
    Heuristic prioritization score for county-campus outreach opportunities.

    This is not a causal model or clinical decision rule. It scales each input,
    then applies the conceptual formula:

    score = current_patient_volume
        + alpha * uninsurance_change
        + beta * hospital_involvement
        - delta * distance_to_campus
    """
    required_columns = [
        "current_patient_volume",
        "uninsurance_change",
        "hospital_involvement",
        "distance_to_campus_miles",
    ]
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise KeyError(f"Campus scoring data is missing required columns: {missing}")

    scored = df.copy()
    scored["current_patient_volume_norm"] = normalize_series(scored["current_patient_volume"])
    scored["uninsurance_change_norm"] = normalize_series(scored["uninsurance_change"])
    scored["hospital_involvement_norm"] = normalize_series(scored["hospital_involvement"])
    scored["distance_to_campus_norm"] = normalize_series(scored["distance_to_campus_miles"])
    scored["campus_opportunity_score"] = (
        scored["current_patient_volume_norm"]
        + alpha * scored["uninsurance_change_norm"]
        + beta * scored["hospital_involvement_norm"]
        - delta * scored["distance_to_campus_norm"]
    )
    return scored.sort_values("campus_opportunity_score", ascending=False).reset_index(drop=True)
