# GeoEarth QA — Portfolio Case Study

**Discipline:** Geospatial AI evaluation engineering  
**Technology:** Python, NumPy, Rasterio, GeoTIFF, pytest, GitHub Actions  
**Project:** Independent prototype; not affiliated with Google or NASA

## Problem

AI systems can produce plausible but numerically incorrect answers to terrain, vegetation, and environmental questions. A useful evaluation requires a transparent reference calculation, clear units and tolerances, and a scoring process that accounts for missing or invalid responses.

## Solution

GeoEarth QA is a Python prototype for **deterministic geospatial reasoning benchmarks**. It includes ten synthetic questions covering slope, relief, NDVI, vegetation fraction, runoff volume, and cardinal direction, plus six reference questions derived from a locally processed Tucson-area digital elevation model (DEM).

The architecture separates:
1. **Data preparation** — a local NASA SRTMGL1 elevation GeoTIFF projected to EPSG:32612 (UTM Zone 12N).
2. **Ground-truth computation** — elevation statistics and Horn 3×3 slope/aspect calculations, with nodata masking and projected-coordinate validation.
3. **Benchmark generation** — machine-readable JSONL questions with explicit answer tolerances.
4. **Blind evaluation export** — prompts without reference answers.
5. **Scoring** — numeric tolerance checks, rejection of non-finite values, and accounting for missing responses.
6. **Quality assurance** — unit tests and an integration test using a synthetic GeoTIFF.

## Demonstrated terrain baseline

A Tucson-area raster (675 × 596 pixels, approximately 27.92 m pixel resolution) produced the following measured reference values:

| Metric | Result |
| --- | ---: |
| Valid elevation pixels | 402,259 |
| Terrain pixels with complete 3×3 neighborhoods | 399,721 |
| Minimum elevation | 669.0 m |
| Maximum elevation | 994.0 m |
| Mean elevation | 754.2979 m |
| Elevation range | 325.0 m |
| Mean slope | 3.4217° |
| Maximum slope | 43.1785° |

**Interpretation:** These figures describe only the selected raster extent. They are not measurements of the whole city of Tucson. The source DEM is not committed to the repository; see [terrain baseline and provenance](tucson_terrain_baseline.md).

## Google Earth visual companion

[Open the Tucson terrain baseline map](https://earth.google.com/web/@32.225,-110.95,736.95117076a,29088.3177254d,30y,0h,0t,0r/data=CgRCAggBMikKJwolCiExSU05bHNlOGt5TUtHeW1sc3kwT3Q0ZVZuQy1qdHlwaEggAToDCgEwQgIIAEoICLynoacBEAE?pli=1) to inspect the approximate study rectangle and a placemark summarizing the local DEM reference calculations. The imported [KML source](tucson_terrain_baseline.kml) is available for inspection. This is a presentation of the measured extent and documentation links; the elevation raster is not overlaid in Google Earth, and the map is not a Google Earth Engine analysis. Google Earth's own on-map elevation estimates may differ from the locally processed raster statistics because they use a different display data source and method.

## Engineering decisions

- **Projected coordinate system:** Slope uses horizontal distances in metres, not longitude/latitude degrees.
- **Nodata handling:** Terrain derivatives are computed only where all cells in a 3×3 neighborhood are valid.
- **Separation of truth and model output:** Reference answers are stored separately from blind prompts.
- **Explicit scoring contract:** Responses use question IDs and answers in JSONL, with numerical tolerances.
- **Offline operation:** The core workflow needs no cloud subscription, credentials, or model API.
- **Reproducible tests:** Synthetic raster fixtures permit pipeline tests without distributing a third-party DEM.

## Evidence and boundaries

The project contains source code, tests, an observed terrain baseline, and reference-question fixtures. The latest automated test run has **not been independently confirmed in this case study**. No AI model was actually evaluated as part of the published terrain baseline; therefore **no model accuracy, comparative ranking, or benchmark-validity claim is made**.

A meaningful future model evaluation must provide each model access to the same DEM and permitted analysis tools, retain the actual model responses and environment, and then score them against the fixed reference answers. Simply asking a model to guess unknown DEM statistics is not a valid test of raster reasoning.

## Portfolio relevance

This project demonstrates the translation of GIS and landscape-analysis domain knowledge into structured AI evaluation: defining measurable tasks, generating independent reference outputs, implementing numerical scoring, controlling data quality, and documenting methodological limits.

**Repository:** https://github.com/dalgreg-ai/geoearth-qa  
**Reference questions:** [Tucson JSONL](../data/tucson_reference_questions.jsonl)  
**Terrain methods:** [Python implementation](../src/raster_terrain.py)  
**Tests:** [Integration test](../tests/test_tucson_integration.py)

## Next milestone (optional)

Run a recorded tool-enabled model evaluation and publish the model/version, permitted data access, raw responses, score report, and failure analysis. This would strengthen the portfolio, but it is not required to present the current prototype as an engineering case study.
