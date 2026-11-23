# GeoEarth QA — System architecture

This diagram describes the implemented prototype, not a live deployed service.

```mermaid
flowchart TD
    A["NASA SRTM elevation DEM<br/>Local GeoTIFF"] --> B["Projected raster<br/>EPSG:32612 / metre units"]
    B --> C["Rasterio + NumPy<br/>Validation, nodata mask, Horn 3×3"]
    C --> D["Terrain statistics<br/>Elevation / slope / aspect"]
    D --> E["Reference question generator<br/>src.tucson_demo"]
    E --> F["Ground truth JSONL<br/>Answers + tolerances"]
    E --> G["Blind prompt export<br/>IDs + questions only"]
    G --> H["External model evaluation<br/>Same data + allowed tools"]
    H --> I["Recorded model responses<br/>JSONL"]
    F --> J["Scoring engine<br/>src.evaluator"]
    I --> J
    J --> K["Accuracy + per-question report"]
    L["Synthetic fixture + pytest"] -.-> C
    L -.-> E
    L -.-> J
```

## What is already implemented

- Local projected-raster analysis, with explicit CRS/unit validation and nodata handling.
- Ground-truth JSONL generation and separate blind-prompt export.
- Scoring with numeric tolerances, duplicate-ID checks, and non-finite-answer handling.
- Unit and integration tests using synthetic raster fixtures.
- A measured Tucson-area baseline and a six-question reference snapshot.

## Not yet demonstrated

The **external model evaluation** box is a *planned manual step*, not an executed integration. No model accuracy has been measured or published. The CI status of the most recent commit also requires verification.

See [portfolio case study](portfolio_case_study.md) and [terrain baseline](tucson_terrain_baseline.md).
