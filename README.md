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
