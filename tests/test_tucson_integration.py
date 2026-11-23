"""Integration tests for offline terrain benchmark and scoring."""
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from src.evaluator import load_jsonl, score
from src.tucson_demo import main


def test_offline_benchmark_end_to_end(tmp_path, monkeypatch):
    dem_path = tmp_path / "synthetic.tif"
    transform = from_origin(500000, 3600000, 30, 30)
    # North-up raster: elevation rises east, producing a westward downslope.
    data = np.tile(np.arange(8, dtype=np.float32) * 3 + 700, (8, 1))
    with rasterio.open(
        dem_path, "w", driver="GTiff", height=8, width=8, count=1,
        dtype="float32", crs="EPSG:32612", transform=transform,
        nodata=-32768,
    ) as ds:
        ds.write(data, 1)

    out = tmp_path / "results"
    monkeypatch.setattr(sys, "argv", [
        "tucson_demo", "--dem", str(dem_path), "--output-dir", str(out),
    ])
    main()
    stats = json.loads((out / "terrain_stats.json").read_text())
    questions = load_jsonl(out / "questions.jsonl")
    assert stats["valid_pixel_count"] == 64
    assert stats["terrain_pixel_count"] == 36
    assert stats["elevation_min_m"] == 700
    assert stats["elevation_max_m"] == 721
    assert abs(stats["slope_mean_degrees"] - np.degrees(np.arctan(0.1))) < 1e-6
    assert len(questions) == 6

    # Simulated responses test scoring mechanics, not model performance.
    responses = [{"id": q["id"], "answer": q["answer"]} for q in questions]
    report = score(questions, responses)
    assert report["total"] == 6
    assert report["correct"] == 6

    responses[0]["answer"] = -9999
    assert score(questions, responses)["correct"] == 5
