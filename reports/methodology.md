# Methodology

## Utilization Indicators

The encounter-level demo data includes binary flags for:

- `is_ed`
- `is_hospital_admittance`
- `is_observation`
- `is_diabetes`

The processing workflow standardizes column names, parses encounter dates, coerces indicator fields to `0/1`, and filters to diabetes-related encounters when building utilization summaries.

## County-Level Aggregation

`src.build_county_panel.build_county_panel()` groups cleaned encounters by county and year. It computes:

- unique diabetes patients
- acute-care event counts
- average distance to the nearest campus
- diabetes acute-care rate

The public demo then merges those utilization summaries with synthetic county context fields such as uninsurance rates and campus distance measures.

## Access-Need Scoring

`src.access_need_score.compute_access_need_score()` normalizes:

- distance to campus
- uninsurance rate change
- diabetes acute-care rate

The default weighted score is:

```text
0.30 * distance
+ 0.35 * uninsurance_change
+ 0.35 * acute_care_rate
```

This score is intended as a heuristic prioritization tool for county-level access need, not a causal estimate.

## Campus Opportunity Scoring

`src.campus_opportunity_score.compute_campus_opportunity_score()` computes a county-campus heuristic using scaled versions of:

- current patient volume
- uninsurance change
- hospital involvement
- distance to campus

Conceptually, the score follows:

```text
score
= current_patient_volume
+ alpha * uninsurance_change
+ beta * hospital_involvement
- delta * distance_to_campus
```

The public implementation rescales each component before combining them so the demo remains numerically stable and easy to interpret.

## Visualization

The public repo intentionally avoids restricted shapefiles and other heavy geospatial dependencies. Instead, it uses shareable bar and line charts to communicate:

- county acute-care utilization trends
- latest-year county access-need scores
- top county-campus opportunity pairs

## Limitations

- The public repo uses synthetic data only.
- County aggregation can hide meaningful patient-level heterogeneity.
- Distance is a proxy for access friction and does not capture transportation reliability, scheduling barriers, or care preferences.
- Insurance context is descriptive and should not be treated as proof of causality.
