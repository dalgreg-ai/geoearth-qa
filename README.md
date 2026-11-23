# GeoEarth QA — Geospatial AI Reasoning Benchmark

An **independent**, reproducible Python prototype for evaluating numerical and spatial reasoning relevant to geographic and environmental workflows. Designed as a technical portfolio project; **not affiliated with Google**.

## What it does

- Generates **10 synthetic, deterministic** evaluation questions on slope, elevation range, NDVI, vegetation fraction, runoff volume and cardinal direction.
- Calculates reference answers independently in Python, with explicit numeric tolerances.
- Scores JSONL model responses, counting unanswered questions as incorrect.
- Provides automated unit tests and GitHub Actions CI.
- Includes an **optional** Google Earth Engine script to calculate mean SRTM terrain slope for an illustrative Tucson-area rectangle. It requires your own approved Google Cloud project and Earth Engine access.

**Limitations:** No LLM is called automatically; the sample benchmark is synthetic and has not been expert-validated. The optional Earth Engine calculation is not used to establish the benchmark's reference answers. It does not evaluate visual satellite-image understanding or certify environmental suitability.

## Quick start (Windows PowerShell)

```powershell
py -m pip install -r requirements.txt
py -m pytest -q
py -m src.benchmark
py -m src.evaluator --responses data/example_responses.jsonl
```

`data/example_responses.jsonl` contains deliberately incomplete demonstration responses; missing responses count as incorrect. The generated report is saved to `results/example_report.json`.

## Response format

One JSON object per line, for example:

```json
{"id":"slope-01","answer":5.7106}
```

## Local Tucson SRTM demonstration (no cloud account required)

The repository includes a reproducible terrain benchmark generator using a **local, projected** GeoTIFF. The source DEM is NASA SRTMGL1 elevation data for an illustrative Tucson-area rectangle (approximately longitude -111.05 to -110.85, latitude 32.15 to 32.30), downloaded through OpenTopography and reprojected to EPSG:32612 (UTM Zone 12N). The raster is not bundled with the source repository.

The independently observed elevation summary for the locally prepared raster was: **669 m minimum, 994 m maximum, 325 m range, 754.30 m mean** (402,259 valid pixels out of 402,300 raster cells; 27.9236 m pixel size). These are measurements of the selected rectangle, **not** the entire Tucson municipality. Terrain slope values are not claimed until the local generator has been executed on the raster.

Place the projected file at `data/dem/tucson_srtm_utm12.tif` and run:

```powershell
py -m pip install -r requirements.txt
py -m pip install rasterio numpy
py -m src.tucson_demo
```

This creates `results/tucson/terrain_stats.json` and `results/tucson/questions.jsonl`. The terrain analyzer uses Horn's 3×3 method, excludes neighborhoods with nodata, and computes slope in degrees from metre-based horizontal distances. It is distinct from the simpler finite-difference exploratory command-line calculation.

To evaluate **actual** model answers, prepare a JSONL response file with matching IDs and numeric `answer` fields, then run:

```powershell
py -m src.evaluator --questions results/tucson/questions.jsonl --responses data/model_responses.jsonl --output results/tucson/model_report.json
```

No model is called automatically; do not interpret generated reference questions as evidence that an AI system has been evaluated. The source raster, download provenance, raster preprocessing, and model identity should be preserved for a fully reproducible comparison.

## Optional Google Earth Engine workflow

```powershell
py -m pip install -r requirements-earthengine.txt
earthengine authenticate
py -m src.earth_engine --project YOUR_GOOGLE_CLOUD_PROJECT_ID
```

The example uses `USGS/SRTMGL1_003` elevation data and `ee.Terrain.slope` for a small illustrative rectangle in Tucson, Arizona. Live outputs depend on Google Earth Engine availability, authorization and dataset access; no live output is included or claimed.

## Roadmap

1. Validate test cases against independent GIS calculations and expert review.
2. Add site metadata, source provenance, uncertainty and reproducible data snapshots.
3. Build a model-adapter layer for repeatable evaluation across multiple LLMs.
4. Add real-data test cases for geospatial reasoning, including controlled spatial joins and raster analysis.

## License

MIT — see `LICENSE`.
