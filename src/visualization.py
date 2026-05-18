from __future__ import annotations

import os
from pathlib import Path

MPL_DIR = Path(__file__).resolve().parents[1] / ".mplconfig"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_DIR))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
