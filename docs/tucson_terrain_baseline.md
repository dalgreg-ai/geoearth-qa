# Tucson SRTM terrain baseline — 2026-11-22

This is a **measured geospatial reference**, not a scored LLM evaluation.

## Source and processing
- Source: NASA SRTMGL1 1-arcsecond elevation raster obtained through OpenTopography.
- Bounding rectangle (approximate): west -111.05°, south 32.15°, east -110.85°, north 32.30°.
- Projected GeoTIFF: EPSG:32612 (UTM zone 12N), bilinear resampling.
- Raster dimensions: 675 columns × 596 rows (402,300 cells).
- Pixel size: approximately 27.923642 m.
- Valid elevation pixels: 402,259.
- Terrain slope pixels with complete 3×3 valid neighborhoods: 399,721.
- Source file used for these measurements: `tucson_srtm_utm12.tif` (not committed to GitHub).

## Measured reference values

| Metric | Result |
| --- | ---: |
| Minimum elevation | 669.0 m |
| Maximum elevation | 994.0 m |
| Elevation range | 325.0 m |
| Mean elevation | 754.2979 m |
| Mean Horn 3×3 slope | 3.4217° |
| Maximum Horn 3×3 slope | 43.1785° |

The slope statistics were calculated using the same 3×3 Horn finite-difference equations and valid-neighborhood mask as `src/raster_terrain.py`. Slope statistics include flat cells but exclude raster-edge cells and cells neighboring nodata.

## Scope and interpretation

These values apply **only** to the specified Tucson-area raster extent. They do not describe the full city, municipal boundary, or metropolitan region. Maximum local slope from a 30 m-class DEM is sensitive to source data, reprojection, and derivative method. The statistics are a computational baseline, not an independent field survey.

## Reproduction and evaluation

Run `py -m src.tucson_demo` with the projected DEM placed at `data/dem/tucson_srtm_utm12.tif`. This writes terrain statistics and six numerical reference questions. To score an actual model, collect its responses separately and use `py -m src.evaluator --questions results/tucson/questions.jsonl --responses YOUR_RESPONSES.jsonl --output results/tucson/model_report.json`.

**No AI model responses have been collected or scored as part of this baseline.** Model accuracy, benchmark validity, and generalization are not claimed.
