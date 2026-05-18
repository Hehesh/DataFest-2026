from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.access_need_score import compute_access_need_score
from src.build_county_panel import build_county_panel
from src.campus_opportunity_score import compute_campus_opportunity_score
from src.clean_encounters import clean_encounters
from src.config import TABLE_DIR, ensure_project_dirs
from src.load_data import load_campus_scores, load_county_panel, load_encounters


def run_processing() -> tuple:
    ensure_project_dirs()

    encounters = clean_encounters(load_encounters(sample=True))
    county_context = load_county_panel(sample=True)
    county_utilization = build_county_panel(encounters)

    county_panel = county_utilization.merge(
        county_context[
            [
                "county_fips",
                "county_name",
                "year",
                "uninsurance_rate",
                "uninsurance_rate_change",
                "distance_to_topeka_miles",
                "distance_to_junction_city_miles",
            ]
        ],
        on=["county_fips", "county_name", "year"],
        how="left",
    )
    county_panel = compute_access_need_score(county_panel)

    campus_scores = compute_campus_opportunity_score(load_campus_scores(sample=True))

    encounters.to_csv(TABLE_DIR / "demo_clean_encounters.csv", index=False)
    county_panel.to_csv(TABLE_DIR / "demo_county_panel.csv", index=False)
    campus_scores.to_csv(TABLE_DIR / "demo_campus_scores.csv", index=False)
    return encounters, county_panel, campus_scores


def main() -> None:
    encounters, county_panel, campus_scores = run_processing()
    print(f"Saved cleaned encounters: {len(encounters)} rows")
    print(f"Saved county panel: {len(county_panel)} rows")
    print(f"Saved campus scores: {len(campus_scores)} rows")


if __name__ == "__main__":
    main()
