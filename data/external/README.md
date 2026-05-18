# External Data

This folder is reserved for public geographic reference data used by the portfolio-safe choropleth workflow.

- `public/kansas_counties.geojson` contains public county boundary geometry for Kansas.
- The choropleth workflow joins synthetic county-level metrics to these geometries using `county_fips`.
- Restricted DataFest data is not included anywhere in this directory.

The default demo pipeline does not require internet access or boundary downloads. Choropleth generation is optional and uses only public geography plus synthetic/sample county data.
