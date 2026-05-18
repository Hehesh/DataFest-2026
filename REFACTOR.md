# REFACTOR.md

## Goal

Refactor the DataFest project repository into a clean, employer-facing portfolio repo that communicates:

1. The analytical story: exploratory data analysis → data processing → figure generation → recommendations.
2. The technical workflow: reusable source code, reproducible scripts, and clear outputs.
3. Responsible data handling: no restricted DataFest or patient-level data committed to GitHub.

This repository should look like a polished data science case study, not a raw competition workspace.

---

## High-Level Decision on Synthetic Data

Include **lightweight synthetic/sample data**, but do **not** attempt to simulate the full original dataset.

Reasoning:

- The original DataFest data is restricted and should not be uploaded.
- A fully realistic synthetic patient dataset would be time-consuming and could create privacy or validity concerns.
- A small schema-matching synthetic sample is enough to show that the code runs and that the project is reproducible.
- The synthetic data should preserve column names, expected data types, and basic value ranges, but it does not need to preserve real distributions.

Implementation target:

- Create small synthetic CSVs with enough rows to run the pipeline end-to-end.
- Make clear in documentation that outputs produced from synthetic data are for demonstration only.
- Keep real analysis outputs, final figures, and final presentation only if competition rules allow sharing them.

---

## Target Repository Structure

Refactor into the following structure:

```text
datafest-svh-access-analysis/
│
├── README.md
├── REFACTOR.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│   └── sample/
│       ├── synthetic_encounters.csv
│       ├── synthetic_county_panel.csv
│       └── synthetic_campus_scores.csv
│
├── notebooks/
│   ├── 01_eda_utilization_patterns.ipynb
│   ├── 02_build_county_panel.ipynb
│   ├── 03_access_need_scoring.ipynb
│   └── 04_generate_final_figures.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── load_data.py
│   ├── clean_encounters.py
│   ├── build_county_panel.py
│   ├── access_need_score.py
│   ├── campus_opportunity_score.py
│   └── visualization.py
│
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── run_processing.py
│   ├── generate_figures.py
│   └── make_all.py
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── reports/
│   ├── executive_summary.md
│   ├── final_presentation.pdf
│   └── methodology.md
│
└── docs/
    ├── data_dictionary.md
    └── limitations.md
```

---

## Refactor Instructions for Codex

### 1. Create the folder structure

Create the folders listed above if they do not already exist.

Add `.gitkeep` files to empty folders only if needed.

---

### 2. Add a safe `.gitignore`

Create or update `.gitignore` so that restricted data and temporary files are not committed.

Suggested `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
.ipynb_checkpoints/
.venv/
venv/
.env

# OS/editor
.DS_Store
.vscode/
.idea/

# Restricted or large data
data/raw/
data/processed/
data/external/
*.parquet
*.feather
*.pickle
*.pkl

# Temporary outputs
outputs/tmp/
```

Do **not** ignore:

```text
data/README.md
data/sample/
outputs/figures/
outputs/tables/
reports/
docs/
```

The portfolio repo should include safe sample data, documentation, and selected final outputs.

---

### 3. Create `data/README.md`

Create a short explanation of the data policy.

Suggested text:

```md
# Data

The original DataFest dataset is not included in this repository due to competition, privacy, and data-use restrictions.

This repository includes small synthetic/sample files in `data/sample/` that mimic the schema of the working data closely enough to demonstrate the project workflow. These files are not intended to reproduce real patient distributions or support substantive healthcare conclusions.

The original analysis used restricted encounter, diagnosis, provider, patient, and geographic data. The public version of this repository focuses on code structure, methodology, and selected shareable outputs.
```

---

### 4. Create lightweight synthetic data

Create `scripts/generate_synthetic_data.py`.

The script should generate the following files:

```text
data/sample/synthetic_encounters.csv
data/sample/synthetic_county_panel.csv
data/sample/synthetic_campus_scores.csv
```

Keep this simple and transparent.

#### Synthetic encounters file

Minimum useful columns:

```text
patient_id
encounter_id
county_fips
county_name
campus
encounter_date
is_diabetes
is_ed
is_hospital_admittance
is_observation
distance_to_nearest_campus_miles
```

Suggested behavior:

- Generate roughly 200–500 synthetic rows.
- Use a few Kansas counties relevant to the project, especially:
  - Shawnee
  - Geary
  - Dickinson
  - Clay
  - Riley
  - Jefferson
  - Osage
  - Wabaunsee
- Include campuses:
  - Topeka
  - Junction City
- Make diabetes, ED, hospital admittance, and observation binary flags.
- Keep values plausible but clearly synthetic.

#### Synthetic county panel file

Minimum useful columns:

```text
county_fips
county_name
year
diabetes_patients
acute_care_events
diabetes_acute_care_rate
uninsurance_rate
uninsurance_rate_change
distance_to_topeka_miles
distance_to_junction_city_miles
```

#### Synthetic campus scores file

Minimum useful columns:

```text
county_fips
county_name
campus
current_patient_volume
uninsurance_change
hospital_involvement
distance_to_campus_miles
campus_opportunity_score
```

Important:

- Add a top-level comment/docstring explaining that this creates demonstration-only data.
- Use a fixed random seed.
- Do not imply that synthetic figures reproduce the original competition findings.

---

### 5. Refactor reusable code into `src/`

Move reusable logic out of notebooks and into source files.

Use these modules:

#### `src/config.py`

Responsibilities:

- Define project paths.
- Define campus coordinates.
- Define selected county labels or constants.
- Define output directories.

Suggested constants:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"

CAMPUSES = {
    "Topeka": {"lon": -95.69, "lat": 39.05},
    "Junction City": {"lon": -96.83, "lat": 39.03},
}
```

#### `src/load_data.py`

Responsibilities:

- Load synthetic/sample data by default.
- Optionally support local restricted data paths if present, but do not require them.
- Fail gracefully with a clear error message if required files are missing.

Core functions:

```python
load_encounters(sample=True)
load_county_panel(sample=True)
load_campus_scores(sample=True)
```

#### `src/clean_encounters.py`

Responsibilities:

- Standardize column names.
- Convert date fields.
- Ensure binary indicator columns are 0/1.
- Filter diabetes-related records when needed.

Core functions:

```python
clean_encounters(df)
filter_diabetes_patients(df)
```

#### `src/build_county_panel.py`

Responsibilities:

- Aggregate encounter-level data to county-level features.
- Calculate patient counts, acute-care counts, and utilization rates.
- Handle missing county FIPS explicitly.

Core functions:

```python
build_county_panel(encounters)
compute_diabetes_acute_care_rate(county_df)
```

#### `src/access_need_score.py`

Responsibilities:

- Compute a county-level access-need score.
- Combine distance, uninsurance change, and acute-care rate.
- Normalize inputs before weighting.

Core functions:

```python
normalize_series(s)
compute_access_need_score(
    county_panel,
    distance_col="distance_to_topeka_miles",
    weights=None
)
```

Default weights can be:

```python
weights = {
    "distance": 0.30,
    "uninsurance_change": 0.35,
    "acute_care_rate": 0.35,
}
```

#### `src/campus_opportunity_score.py`

Responsibilities:

- Score county-campus opportunity.
- Combine current patient volume, uninsurance change, hospital involvement, and distance.

Core function:

```python
compute_campus_opportunity_score(
    df,
    alpha=1.0,
    beta=1.0,
    delta=0.5
)
```

Use the conceptual formula:

```text
score_{county,campus}
= current_patient_volume
+ alpha * uninsurance_change
+ beta * hospital_involvement
- delta * distance_to_campus
```

Document that the formula is a heuristic prioritization score, not a causal model.

#### `src/visualization.py`

Responsibilities:

- Generate clean figures for the portfolio repo.
- Save figures to `outputs/figures/`.
- Keep plotting functions reusable.

Core functions:

```python
plot_diabetes_utilization_trends(df, output_path)
plot_access_need_bar_chart(county_panel, output_path)
plot_campus_opportunity_scores(campus_scores, output_path)
```

If geographic shapefiles are unavailable or restricted, use bar charts or simplified county-level plots for the public repo. Do not make shapefiles a hard dependency unless they are public and documented.

---

### 6. Clean the notebooks

The notebooks should become readable narrative files, not giant code dumps.

Rename or create:

```text
notebooks/01_eda_utilization_patterns.ipynb
notebooks/02_build_county_panel.ipynb
notebooks/03_access_need_scoring.ipynb
notebooks/04_generate_final_figures.ipynb
```

Each notebook should follow this pattern:

```md
# Title

## Purpose
One short paragraph explaining what this notebook does.

## Inputs
List input files.

## Outputs
List figures/tables created.

## Main Steps
1. Load data
2. Clean or transform data
3. Compute metrics
4. Generate outputs
5. Brief interpretation
```

Move as much repeated logic as possible into `src/`.

Notebook code should mostly call functions from `src/`.

---

### 7. Add runnable scripts

Create scripts so a reviewer can reproduce the demo workflow without opening notebooks.

#### `scripts/run_processing.py`

Responsibilities:

- Load synthetic encounters.
- Clean encounters.
- Build county panel.
- Save processed demo tables to `outputs/tables/`.

#### `scripts/generate_figures.py`

Responsibilities:

- Load synthetic/sample or processed demo data.
- Generate selected public-facing figures.
- Save to `outputs/figures/`.

#### `scripts/make_all.py`

Responsibilities:

Run the full safe demo pipeline:

1. Generate synthetic data.
2. Run processing.
3. Generate figures.

Expected command:

```bash
python scripts/make_all.py
```

---

### 8. Create employer-facing documentation

#### `README.md`

Write the README as the main portfolio landing page.

Suggested structure:

```md
# DataFest 2026: Stormont Vail Health Access & Utilization Analysis

## Overview
Briefly explain the project and stakeholder context.

## Research Questions
1. Where are acute-care utilization patterns concentrated?
2. Which counties show high access need?
3. How might Stormont Vail Health prioritize campus-level outreach and planning?

## Analytical Workflow
1. Exploratory data analysis
2. County-level feature construction
3. Access-need scoring
4. Campus opportunity scoring
5. Figure generation and recommendations

## Key Technical Contributions
- Built a county-level analytical panel from healthcare encounter and geographic features.
- Engineered utilization indicators for ED visits, hospital admissions, and observation stays.
- Designed an access-need score combining distance, insurance changes, and acute-care utilization.
- Generated county and campus-level visualizations for stakeholder-facing recommendations.
- Created a privacy-safe synthetic-data version of the workflow.

## Repository Structure
Briefly describe each folder.

## Reproducing the Demo
Explain:

```bash
pip install -r requirements.txt
python scripts/make_all.py
```

## Data Privacy
Explain that the original DataFest data is not included.

## Limitations
Mention:
- Observational analysis, not causal inference.
- Missing geographic identifiers such as CensusBlockFIPS limited some patient-county linkage.
- Synthetic data is for demonstration only.
- Scores are prioritization heuristics, not clinical decision rules.
```

#### `reports/executive_summary.md`

Create a concise 1-page summary:

Sections:

```md
# Executive Summary

## Problem
## Approach
## Key Findings
## Recommendations
## Caveats
```

#### `reports/methodology.md`

Describe:

- How utilization indicators were defined.
- How county-level aggregation was done.
- How access-need scores were computed.
- How campus opportunity scores were computed.
- What limitations apply.

#### `docs/data_dictionary.md`

Document all public/synthetic columns.

Use a table:

```md
| Column | File | Type | Description |
|---|---|---|---|
| patient_id | synthetic_encounters.csv | string | Synthetic patient identifier |
```

#### `docs/limitations.md`

Include a thoughtful limitations section:

- Restricted data cannot be shared publicly.
- Synthetic data does not reproduce real patient distributions.
- Missing CensusBlockFIPS limited geographic linkage.
- County-level aggregation can hide patient-level heterogeneity.
- Distance is only a proxy for access friction.
- Uninsurance changes are contextual, not proof of causality.
- Access-need and opportunity scores are prioritization tools, not causal estimates or clinical recommendations.

---

### 9. Requirements file

Create a minimal `requirements.txt`.

Suggested:

```text
numpy
pandas
matplotlib
jupyter
```

Only add packages actually used.

If geospatial plotting is retained, add:

```text
geopandas
shapely
pyproj
contextily
```

But avoid geospatial dependencies in the default demo unless necessary, because they can make installation harder for reviewers.

---

### 10. Output policy

The repo may include:

```text
outputs/figures/
outputs/tables/
reports/
docs/
```

But it should not include:

```text
data/raw/
data/processed/ with restricted data
patient-level real data
competition-provided confidential files
private notes containing sensitive details
```

If final figures are derived from restricted data, only include them if the DataFest rules allow public sharing. Otherwise, regenerate demo figures from synthetic data and label them as demonstration outputs.

---

## Suggested Final Deliverables

After refactoring, the repo should support the following reviewer experience:

```bash
git clone <repo>
cd datafest-svh-access-analysis
pip install -r requirements.txt
python scripts/make_all.py
```

This should create or refresh:

```text
data/sample/synthetic_encounters.csv
data/sample/synthetic_county_panel.csv
data/sample/synthetic_campus_scores.csv
outputs/tables/
outputs/figures/
```

A reviewer should then be able to read:

```text
README.md
reports/executive_summary.md
reports/methodology.md
docs/data_dictionary.md
docs/limitations.md
```

without needing access to the restricted DataFest data.

---

## Quality Bar

The refactor is complete when:

- No restricted data is committed.
- The README explains the project clearly in under two minutes of reading.
- The demo pipeline runs from a clean clone.
- The notebooks are clean, numbered, and narrative-driven.
- Reusable logic lives in `src/`, not copied across notebooks.
- Synthetic data is clearly labeled as synthetic.
- Figures and methodology communicate the stakeholder-facing story.
- Limitations are explicit and credible.
