# Limitations

- Restricted Data: The original DataFest data cannot be shared publicly, so this repository relies on synthetic sample files for reproducibility.
- Synthetic Demonstration: The sample data preserves schema and plausible value ranges, but it does not reproduce real patient distributions, care pathways, or outcome patterns.
- Geographic Linkage: In the original project setting, missing identifiers such as `CensusBlockFIPS` can limit patient-county linkage and downstream spatial interpretation.
- Aggregation Loss: County-level summaries can hide meaningful patient-level heterogeneity and within-county variation.
- Distance Proxy: Distance to campus is only a rough proxy for access friction and does not capture transportation reliability, appointment availability, referral patterns, or patient preference.
- Context, Not Causality: Uninsurance trends and utilization rates help describe context, but they do not establish causality.
- Score Interpretation: Access-need and campus-opportunity scores are prioritization heuristics, not causal estimates, operational forecasts, or clinical recommendations.
