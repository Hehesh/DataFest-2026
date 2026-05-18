from __future__ import annotations

import os
from pathlib import Path

MPL_DIR = Path(__file__).resolve().parents[1] / ".mplconfig"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import pandas as pd


def _apply_portfolio_style() -> None:
    plt.style.use("default")
    plt.rcParams.update(
        {
            "axes.facecolor": "#F8F4ED",
            "figure.facecolor": "#FFFDF8",
            "axes.edgecolor": "#5B4636",
            "axes.labelcolor": "#2B2118",
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "font.size": 10,
            "grid.color": "#DCCBB6",
            "grid.alpha": 0.6,
            "text.color": "#2B2118",
            "xtick.color": "#2B2118",
            "ytick.color": "#2B2118",
            "savefig.bbox": "tight",
        }
    )


def _get_geopandas():
    try:
        import geopandas as gpd
    except ImportError as exc:
        raise ImportError(
            "geopandas is required for choropleth maps. "
            "Install with: pip install -r requirements-geo.txt"
        ) from exc
    return gpd


def load_county_geometries(path: str | Path):
    gpd = _get_geopandas()
    geometry_path = Path(path)
    if not geometry_path.exists():
        raise FileNotFoundError(f"Missing county geometry file: {geometry_path}")
    geo = gpd.read_file(geometry_path)
    if "county_fips" not in geo.columns:
        if "id" in geo.columns:
            geo["county_fips"] = geo["id"].astype(str).str.zfill(5)
        elif {"STATE", "COUNTY"}.issubset(geo.columns):
            geo["county_fips"] = (
                geo["STATE"].astype(str).str.zfill(2) + geo["COUNTY"].astype(str).str.zfill(3)
            )
        else:
            raise KeyError("County geometry file must include county_fips or state/county code fields.")

    if "county_name" not in geo.columns and "NAME" in geo.columns:
        geo["county_name"] = geo["NAME"].astype(str).str.strip()

    geo["county_fips"] = geo["county_fips"].astype(str).str.strip().str.zfill(5)
    keep_cols = [column for column in ["county_fips", "county_name", "geometry"] if column in geo.columns]
    geo = geo[keep_cols].copy()
    return geo


def prepare_county_choropleth_data(
    county_panel: pd.DataFrame,
    county_geo,
    fips_col: str = "county_fips",
):
    plot_df = county_panel.copy()
    plot_df[fips_col] = (
        plot_df[fips_col].astype(str).str.strip().str.replace(r"\.0$", "", regex=True).str.zfill(5)
    )
    plot_df = plot_df.drop_duplicates(subset=[fips_col]).copy()
    merged = county_geo.merge(
        plot_df,
        left_on="county_fips",
        right_on=fips_col,
        how="left",
        suffixes=("_geo", ""),
    )
    if "county_name" not in merged.columns and "county_name_geo" in merged.columns:
        merged["county_name"] = merged["county_name_geo"]
    elif "county_name_geo" in merged.columns:
        merged["county_name"] = merged["county_name"].fillna(merged["county_name_geo"])
    return merged


def plot_county_choropleth(
    county_panel: pd.DataFrame,
    county_geo,
    value_col: str,
    output_path: str | Path,
    title: str,
    cmap: str = "Blues",
    label_col: str = "county_name",
    annotate_counties: dict[str, dict[str, float | str]] | None = None,
    fips_col: str = "county_fips",
    vmin: float | None = None,
    vmax: float | None = None,
):
    _apply_portfolio_style()
    merged = prepare_county_choropleth_data(county_panel, county_geo, fips_col=fips_col)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if value_col not in merged.columns:
        raise KeyError(f"Value column '{value_col}' not found in choropleth data.")

    numeric_values = pd.to_numeric(merged[value_col], errors="coerce")
    plot_vmin = float(numeric_values.min()) if vmin is None and numeric_values.notna().any() else vmin
    plot_vmax = float(numeric_values.max()) if vmax is None and numeric_values.notna().any() else vmax

    fig, ax = plt.subplots(figsize=(8.8, 6.2))
    norm = Normalize(vmin=plot_vmin, vmax=plot_vmax)

    merged.plot(
        column=value_col,
        ax=ax,
        cmap=cmap,
        linewidth=0.6,
        edgecolor="#F2EEE8",
        legend=False,
        missing_kwds={"color": "#D9D7D2", "label": "Missing"},
        vmin=plot_vmin,
        vmax=plot_vmax,
    )

    merged.boundary.plot(ax=ax, linewidth=0.35, color="#FFFDF8")
    ax.set_title(title, pad=12)
    ax.set_axis_off()

    sm = ScalarMappable(norm=norm, cmap=plt.get_cmap(cmap))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02)
    cbar.outline.set_linewidth(0.4)
    cbar.set_label(value_col.replace("_", " ").title())

    if annotate_counties:
        points = merged.set_index("county_fips").geometry.representative_point()
        for county_fips, config in annotate_counties.items():
            if county_fips not in points.index:
                continue
            point = points.loc[county_fips]
            label = str(config.get("name", county_fips))
            dx = float(config.get("dx", 0.0))
            dy = float(config.get("dy", 0.0))
            ax.text(
                point.x + dx,
                point.y + dy,
                label,
                fontsize=8,
                color="#2B2118",
                ha="left",
                va="center",
                bbox={"facecolor": "#FFFDF8", "edgecolor": "none", "alpha": 0.85, "pad": 1.5},
            )

    fig.savefig(output, dpi=180)
    plt.close(fig)
    return ax


def plot_diabetes_utilization_trends(df: pd.DataFrame, output_path: str | Path) -> None:
    _apply_portfolio_style()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    plot_df = (
        df.groupby(["county_name", "year"], as_index=False)["diabetes_acute_care_rate"]
        .mean()
        .sort_values(["county_name", "year"])
    )
    top_counties = (
        plot_df.groupby("county_name")["diabetes_acute_care_rate"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index
    )
    plot_df = plot_df[plot_df["county_name"].isin(top_counties)]

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = ["#8C2F39", "#1D4E89", "#2E6F40", "#C17C2F", "#6A3D9A"]

    for color, county in zip(palette, sorted(plot_df["county_name"].unique())):
        county_df = plot_df[plot_df["county_name"] == county]
        ax.plot(
            county_df["year"],
            county_df["diabetes_acute_care_rate"],
            marker="o",
            linewidth=2.5,
            color=color,
            label=county,
        )

    ax.set_title("Synthetic Diabetes Acute-Care Rate by County")
    ax.set_xlabel("Year")
    ax.set_ylabel("Acute-care events per 100 diabetes patients")
    ax.grid(axis="y")
    ax.legend(frameon=False, ncols=2)
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_access_need_bar_chart(county_panel: pd.DataFrame, output_path: str | Path) -> None:
    _apply_portfolio_style()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    latest_year = county_panel["year"].max()
    plot_df = county_panel[county_panel["year"] == latest_year].sort_values("access_need_score")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(plot_df["county_name"], plot_df["access_need_score"], color="#8C2F39")
    ax.set_title(f"Access-Need Score by County ({latest_year})")
    ax.set_xlabel("Heuristic access-need score")
    ax.set_ylabel("County")
    ax.grid(axis="x")
    fig.savefig(output, dpi=180)
    plt.close(fig)


def plot_campus_opportunity_scores(campus_scores: pd.DataFrame, output_path: str | Path) -> None:
    _apply_portfolio_style()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    plot_df = campus_scores.copy()
    plot_df["label"] = plot_df["county_name"] + " - " + plot_df["campus"]
    plot_df = plot_df.sort_values("campus_opportunity_score").tail(10)

    color_map = {"Topeka": "#1D4E89", "Junction City": "#C17C2F"}
    colors = [color_map.get(campus, "#5B4636") for campus in plot_df["campus"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(plot_df["label"], plot_df["campus_opportunity_score"], color=colors)
    ax.set_title("Top Synthetic County-Campus Opportunity Scores")
    ax.set_xlabel("Heuristic opportunity score")
    ax.set_ylabel("County-Campus pair")
    ax.grid(axis="x")
    fig.savefig(output, dpi=180)
    plt.close(fig)


def create_demo_presentation_pdf(
    encounter_count: int,
    county_panel: pd.DataFrame,
    campus_scores: pd.DataFrame,
    output_path: str | Path,
) -> None:
    _apply_portfolio_style()
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    latest_counties = county_panel[county_panel["year"] == county_panel["year"].max()]
    highest_need = latest_counties.sort_values("access_need_score", ascending=False).iloc[0]
    highest_opportunity = campus_scores.sort_values(
        "campus_opportunity_score",
        ascending=False,
    ).iloc[0]

    fig = plt.figure(figsize=(11, 8.5))
    fig.patch.set_facecolor("#FFFDF8")
    fig.text(0.08, 0.92, "Stormont Vail Access & Utilization Analysis", fontsize=22, weight="bold")
    fig.text(0.08, 0.875, "Public demo summary built from synthetic data only", fontsize=12, color="#5B4636")

    summary_lines = [
        f"Synthetic encounters generated: {encounter_count}",
        f"Counties covered: {latest_counties['county_name'].nunique()}",
        f"Highest access-need county in the latest year: {highest_need['county_name']}",
        "Priority drivers: distance, uninsurance change, acute-care utilization",
        (
            "Highest county-campus opportunity pair: "
            f"{highest_opportunity['county_name']} - {highest_opportunity['campus']}"
        ),
        "Opportunity score is a heuristic for outreach prioritization, not a causal model",
    ]

    y = 0.78
    for line in summary_lines:
        fig.text(0.10, y, f"- {line}", fontsize=13)
        y -= 0.08

    fig.text(
        0.08,
        0.14,
        "This PDF is included as a public-facing stand-in for a competition presentation. "
        "It intentionally avoids restricted data and real patient-level results.",
        fontsize=11,
        color="#5B4636",
    )
    fig.savefig(output)
    plt.close(fig)
