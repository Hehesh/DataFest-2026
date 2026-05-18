from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import FIGURE_DIR, REPORT_DIR, TABLE_DIR, ensure_project_dirs
from src.visualization import (
    create_demo_presentation_pdf,
    plot_access_need_bar_chart,
    plot_campus_opportunity_scores,
    plot_diabetes_utilization_trends,
)


def _load_or_fail(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {label} at {path}. Run `python scripts/run_processing.py` first."
        )
    return pd.read_csv(path)


def generate_figures() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_project_dirs()

    encounters = _load_or_fail(TABLE_DIR / "demo_clean_encounters.csv", "cleaned encounter table")
    county_panel = _load_or_fail(TABLE_DIR / "demo_county_panel.csv", "county panel")
    campus_scores = _load_or_fail(TABLE_DIR / "demo_campus_scores.csv", "campus scores")

    plot_diabetes_utilization_trends(
        county_panel,
        FIGURE_DIR / "diabetes_utilization_trends.png",
    )
    plot_access_need_bar_chart(
        county_panel,
        FIGURE_DIR / "access_need_scores.png",
    )
    plot_campus_opportunity_scores(
        campus_scores,
        FIGURE_DIR / "campus_opportunity_scores.png",
    )
    create_demo_presentation_pdf(
        encounter_count=len(encounters),
        county_panel=county_panel,
        campus_scores=campus_scores,
        output_path=REPORT_DIR / "final_presentation.pdf",
    )
    return encounters, county_panel, campus_scores


def main() -> None:
    _, county_panel, campus_scores = generate_figures()
    print(f"Generated figures for {county_panel['county_name'].nunique()} counties")
    print(f"Generated campus opportunity plot with {len(campus_scores)} rows")


if __name__ == "__main__":
    main()
