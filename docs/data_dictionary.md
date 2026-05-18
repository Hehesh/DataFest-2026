# Data Dictionary

| Column | File | Type | Description |
|---|---|---|---|
| patient_id | `synthetic_encounters.csv` | string | Synthetic patient identifier |
| encounter_id | `synthetic_encounters.csv` | string | Synthetic encounter identifier |
| county_fips | `synthetic_encounters.csv` | string | Five-digit county FIPS code |
| county_name | `synthetic_encounters.csv` | string | County label used in plots and tables |
| campus | `synthetic_encounters.csv` | string | Campus associated with the synthetic encounter |
| encounter_date | `synthetic_encounters.csv` | date | Synthetic encounter date |
| is_diabetes | `synthetic_encounters.csv` | integer | Binary flag for diabetes-related encounter |
| is_ed | `synthetic_encounters.csv` | integer | Binary flag for emergency department encounter |
| is_hospital_admittance | `synthetic_encounters.csv` | integer | Binary flag for hospital admission |
| is_observation | `synthetic_encounters.csv` | integer | Binary flag for observation stay |
| distance_to_nearest_campus_miles | `synthetic_encounters.csv` | float | Approximate miles to the nearest campus |
| county_fips | `synthetic_county_panel.csv` | string | Five-digit county FIPS code |
| county_name | `synthetic_county_panel.csv` | string | County label |
| year | `synthetic_county_panel.csv` | integer | Calendar year |
| diabetes_patients | `synthetic_county_panel.csv` | integer | Synthetic count of diabetes-related patients |
| acute_care_events | `synthetic_county_panel.csv` | integer | Synthetic count of acute-care events |
| diabetes_acute_care_rate | `synthetic_county_panel.csv` | float | Acute-care events per 100 diabetes patients |
| uninsurance_rate | `synthetic_county_panel.csv` | float | Synthetic county uninsurance rate |
| uninsurance_rate_change | `synthetic_county_panel.csv` | float | Synthetic year-over-year contextual change in uninsurance |
| distance_to_topeka_miles | `synthetic_county_panel.csv` | float | Approximate county distance to the Topeka campus |
| distance_to_junction_city_miles | `synthetic_county_panel.csv` | float | Approximate county distance to the Junction City campus |
| county_fips | `synthetic_campus_scores.csv` | string | Five-digit county FIPS code |
| county_name | `synthetic_campus_scores.csv` | string | County label |
| campus | `synthetic_campus_scores.csv` | string | Campus being evaluated |
| current_patient_volume | `synthetic_campus_scores.csv` | integer | Synthetic current patient volume tied to the county-campus pair |
| uninsurance_change | `synthetic_campus_scores.csv` | float | Synthetic contextual uninsurance change carried into the campus score |
| hospital_involvement | `synthetic_campus_scores.csv` | float | Synthetic share-like indicator for hospital involvement |
| distance_to_campus_miles | `synthetic_campus_scores.csv` | float | Approximate county distance to the evaluated campus |
| campus_opportunity_score | `synthetic_campus_scores.csv` | float | Heuristic county-campus opportunity score |
| year | `demo_county_panel.csv` | integer | Year carried into processed county summaries |
| average_distance_to_nearest_campus | `demo_county_panel.csv` | float | Mean synthetic encounter distance among diabetes encounters |
| distance_norm | `demo_county_panel.csv` | float | Min-max scaled distance component |
| uninsurance_change_norm | `demo_county_panel.csv` | float | Min-max scaled uninsurance change component |
| acute_care_rate_norm | `demo_county_panel.csv` | float | Min-max scaled acute-care rate component |
| access_need_score | `demo_county_panel.csv` | float | Heuristic county access-need score |
| current_patient_volume_norm | `demo_campus_scores.csv` | float | Min-max scaled current volume component |
| hospital_involvement_norm | `demo_campus_scores.csv` | float | Min-max scaled hospital involvement component |
| distance_to_campus_norm | `demo_campus_scores.csv` | float | Min-max scaled distance component for campus scoring |
| county_fips | `demo_county_panel.csv` and `demo_campus_scores.csv` | string | Join key used for choropleth mapping; loaded as a five-digit FIPS code |
| county_name | `demo_county_panel.csv` and `demo_campus_scores.csv` | string | Public county label used for tables and optional annotations |
| diabetes_acute_care_rate | `demo_county_panel.csv` | float | Processed diabetes acute-care events per 100 diabetes patients |
| uninsurance_rate_change | `demo_county_panel.csv` | float | Processed contextual uninsurance change used in the access-need score |
| access_need_score | `demo_county_panel.csv` | float | Heuristic county access-need score used in bar charts and choropleths |
| campus_opportunity_score | `demo_campus_scores.csv` | float | Heuristic county-campus opportunity score used in bar charts and choropleths |
| geometry | `kansas_counties.geojson` | geometry | Public Kansas county boundary geometry used for optional choropleth maps |
| county_fips | `kansas_counties.geojson` | string | Five-digit county FIPS key derived from the public boundary source |
| county_name | `kansas_counties.geojson` | string | County label supplied by the public boundary source |
