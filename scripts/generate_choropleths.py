from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_processing import run_processing
from src.config import FIGURE_DIR, KANSAS_COUNTIES_GEOJSON, TABLE_DIR, ensure_project_dirs
from src.visualization import load_county_geometries, plot_county_choropleth

KEY_COUNTY_ANNOTATIONS = {
    "20177": {"name": "Shawnee", "dx": 0.08, "dy": 0.02},
    "20061": {"name": "Geary", "dx": 0.06, "dy": -0.02},
    "20041": {"name": "Dickinson", "dx": 0.05, "dy": 0.03},
    "20027": {"name": "Clay", "dx": 0.04, "dy": 0.03},
}


def _load_or_build_demo_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    county_path = TABLE_DIR / "demo_county_panel.csv"
    campus_path = TABLE_DIR / "demo_campus_scores.csv"
    if county_path.exists() and campus_path.exists():
        county_panel = pd.read_csv(county_path, dtype={"county_fips": "string"})
        campus_scores = pd.read_csv(campus_path, dtype={"county_fips": "string"})
        return county_panel, campus_scores

    _, county_panel, campus_scores = run_processing()
    county_panel["county_fips"] = county_panel["county_fips"].astype(str).str.zfill(5)
    campus_scores["county_fips"] = campus_scores["county_fips"].astype(str).str.zfill(5)
    return county_panel, campus_scores


def generate_choropleths(annotate: bool = False) -> None:
    ensure_project_dirs()

    try:
        county_geo = load_county_geometries(KANSAS_COUNTIES_GEOJSON)
    except ImportError as exc:
        raise SystemExit(str(exc)) from exc
    except FileNotFoundError as exc:
        raise SystemExit(
            "Missing public county boundary file. Expected: "
            "data/external/public/kansas_counties.geojson. "
            "Add a public Kansas county GeoJSON or run the optional boundary preparation step."
        ) from exc

    if not KANSAS_COUNTIES_GEOJSON.exists():
        raise SystemExit(
            "Missing public county boundary file. Expected: "
            "data/external/public/kansas_counties.geojson. "
            "Add a public Kansas county GeoJSON or run the optional boundary preparation step."
        )

    county_panel, campus_scores = _load_or_build_demo_tables()
    latest_year = int(county_panel["year"].max())
    latest_county_panel = county_panel[county_panel["year"] == latest_year].copy()
    annotations = KEY_COUNTY_ANNOTATIONS if annotate else None

    plot_county_choropleth(
        latest_county_panel,
        county_geo,
        value_col="access_need_score",
        output_path=FIGURE_DIR / "choropleth_access_need_score.png",
        title=f"Synthetic Access-Need Score by County ({latest_year})",
        cmap="Purples",
        annotate_counties=annotations,
    )
    plot_county_choropleth(
        latest_county_panel,
        county_geo,
        value_col="diabetes_acute_care_rate",
        output_path=FIGURE_DIR / "choropleth_diabetes_acute_care_rate.png",
        title=f"Synthetic Diabetes Acute-Care Rate by County ({latest_year})",
        cmap="Blues",
        annotate_counties=annotations,
    )
    plot_county_choropleth(
        latest_county_panel,
        county_geo,
        value_col="uninsurance_rate_change",
        output_path=FIGURE_DIR / "choropleth_uninsurance_rate_change.png",
        title=f"Synthetic Uninsurance Rate Change by County ({latest_year})",
        cmap="BuPu",
        annotate_counties=annotations,
    )

    campus_min = float(campus_scores["campus_opportunity_score"].min())
    campus_max = float(campus_scores["campus_opportunity_score"].max())
    for campus_name, output_name in [
        ("Topeka", "choropleth_topeka_opportunity_score.png"),
        ("Junction City", "choropleth_junction_city_opportunity_score.png"),
    ]:
        campus_df = campus_scores[campus_scores["campus"] == campus_name].copy()
        plot_county_choropleth(
            campus_df,
            county_geo,
            value_col="campus_opportunity_score",
            output_path=FIGURE_DIR / output_name,
            title=f"Synthetic {campus_name} Opportunity Score by County",
            cmap="PuBu",
            annotate_counties=annotations,
            vmin=campus_min,
            vmax=campus_max,
        )


def main() -> None:
    annotate = "--annotate-key-counties" in sys.argv
    generate_choropleths(annotate=annotate)
    print("Generated optional choropleth figures in outputs/figures/.")


if __name__ == "__main__":
    main()
