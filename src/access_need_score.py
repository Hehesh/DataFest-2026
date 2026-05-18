from __future__ import annotations

import pandas as pd


def normalize_series(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    minimum = numeric.min()
    maximum = numeric.max()
    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(0.0, index=series.index, dtype="float64")
    if minimum == maximum:
        return pd.Series(0.0, index=series.index, dtype="float64")
    return (numeric - minimum) / (maximum - minimum)


def compute_access_need_score(
    county_panel: pd.DataFrame,
    distance_col: str = "distance_to_topeka_miles",
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    score_weights = weights or {
        "distance": 0.30,
        "uninsurance_change": 0.35,
        "acute_care_rate": 0.35,
    }

    required_columns = [
        distance_col,
        "uninsurance_rate_change",
        "diabetes_acute_care_rate",
    ]
    missing = [column for column in required_columns if column not in county_panel.columns]
    if missing:
        raise KeyError(f"County panel is missing required scoring columns: {missing}")

    scored = county_panel.copy()
    scored["distance_norm"] = normalize_series(scored[distance_col])
    scored["uninsurance_change_norm"] = normalize_series(scored["uninsurance_rate_change"])
    scored["acute_care_rate_norm"] = normalize_series(scored["diabetes_acute_care_rate"])
    scored["access_need_score"] = (
        scored["distance_norm"] * score_weights["distance"]
        + scored["uninsurance_change_norm"] * score_weights["uninsurance_change"]
        + scored["acute_care_rate_norm"] * score_weights["acute_care_rate"]
    )
    return scored.sort_values(["year", "access_need_score"], ascending=[True, False]).reset_index(drop=True)
