# DataFest 2026: Stormont Vail Health Access & Utilization Analysis

## Overview

This repository packages a privacy-safe, employer-facing version of an ASA DataFest 2026 healthcare analytics project for Stormont Vail Health. The original work explored how diabetes-related utilization, county access conditions, and campus geography could be combined into a practical planning story for outreach and service delivery.

The public repo keeps the analytical workflow intact while replacing restricted source data with lightweight synthetic files that let reviewers run the demo end to end.

## Research Questions

1. Where are diabetes-related acute-care utilization patterns concentrated?
2. Which counties show elevated access need when distance, insurance context, and utilization are considered together?
3. How might Stormont Vail Health prioritize county-campus outreach opportunities?

## Analytical Workflow

1. Exploratory data analysis
2. County-level feature construction
3. Access-need scoring
4. Campus opportunity scoring
5. Figure generation and recommendations

## Key Technical Contributions

- Built a county-level analytical panel from healthcare encounter and geographic features.
- Engineered utilization indicators for ED visits, hospital admissions, and observation stays.
- Designed an access-need score combining distance, uninsurance changes, and acute-care utilization.
- Generated county and campus-level visualizations for stakeholder-facing recommendations.
- Created a privacy-safe synthetic-data version of the workflow.

## Repository Structure

- `data/`: data policy notes plus small synthetic CSVs for the public demo
- `src/`: reusable data loading, cleaning, scoring, and plotting code
- `scripts/`: command-line entry points for generating data, processing tables, and making figures
- `notebooks/`: short narrative notebooks that call into `src/`
- `outputs/`: demo figures and processed tables
- `reports/`: executive summary, methodology notes, and a synthetic demo PDF
- `docs/`: data dictionary and limitations

## Reproducing the Demo

```bash
pip install -r requirements.txt
python scripts/make_all.py
```

That workflow regenerates:

- `data/sample/synthetic_encounters.csv`
- `data/sample/synthetic_county_panel.csv`
- `data/sample/synthetic_campus_scores.csv`
- `outputs/tables/demo_clean_encounters.csv`
- `outputs/tables/demo_county_panel.csv`
- `outputs/tables/demo_campus_scores.csv`
- `outputs/figures/*.png`
- `reports/final_presentation.pdf`

## Generating Choropleth Maps

Map generation is optional because it depends on geospatial packages and a public county boundary file.

```bash
pip install -r requirements.txt
pip install -r requirements-geo.txt
python scripts/generate_choropleths.py
```

Or run the core demo plus optional maps in one step:

```bash
python scripts/make_all.py --with-maps
```

Expected choropleth outputs include:

- `outputs/figures/choropleth_access_need_score.png`
- `outputs/figures/choropleth_diabetes_acute_care_rate.png`
- `outputs/figures/choropleth_uninsurance_rate_change.png`
- `outputs/figures/choropleth_topeka_opportunity_score.png`
- `outputs/figures/choropleth_junction_city_opportunity_score.png`

These maps are generated from synthetic/sample data in the public repo and joined to public Kansas county geometry by `county_fips`. Original competition choropleths should only be shared if DataFest rules explicitly allow it.

## Data Privacy

The original DataFest data is not included in this repository. No restricted encounter-level or patient-level source files are required for the public demo, and the sample data in `data/sample/` is synthetic by design.

## Limitations

- This is an observational analysis, not causal inference.
- Synthetic data is for demonstration only and does not reproduce real patient distributions.
- Missing geographic identifiers such as `CensusBlockFIPS` can limit patient-county linkage in real-world workflows.
- Access-need and campus-opportunity scores are prioritization heuristics, not clinical decision rules.
