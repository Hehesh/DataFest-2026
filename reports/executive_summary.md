# Executive Summary

## Problem

Stormont Vail Health needed a clearer view of where diabetes-related utilization pressure and access friction may be concentrated across its service region, and how that picture could inform campus-level outreach or planning.

## Approach

The project combined encounter-level utilization indicators with county context and campus distance measures. In the public version of the repository, the same workflow is demonstrated with synthetic data: clean encounter records, aggregate to a county panel, compute access-need scores, score county-campus opportunities, and generate presentation-ready figures.

## Key Findings

The synthetic demo consistently surfaces a small group of counties where three signals align: longer travel distance, worsening uninsurance context, and higher acute-care utilization among diabetes-related encounters. It also shows how county-campus opportunity scoring can distinguish between counties that are high need overall and counties that may be better suited to a specific campus outreach strategy.

## Recommendations

- Use county-level scores as a planning shortlist, not a final ranking.
- Pair utilization metrics with local operational knowledge before acting.
- Treat campus opportunity scores as a way to organize outreach discussions around service area coverage, not as a causal forecast.
- Maintain a privacy-safe demo pipeline so the methodology can be shared without exposing restricted data.

## Caveats

This portfolio repo does not include the original restricted DataFest data. All sample data and resulting outputs are synthetic and should be interpreted as workflow demonstrations only.
