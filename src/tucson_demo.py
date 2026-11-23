"""Generate a reproducible local SRTM terrain evaluation case.

No cloud services, API keys, or LLM calls are required.
"""
import argparse
import json
from pathlib import Path

from src.raster_terrain import analyze_dem


def build_questions(stats: dict) -> list[dict]:
    """Numerical ground-truth questions with explicit units and tolerances."""
    fields = [
        ("elevation-min", "What is the minimum elevation in the supplied DEM (metres)?", "elevation_min_m", 1.0),
        ("elevation-max", "What is the maximum elevation in the supplied DEM (metres)?", "elevation_max_m", 1.0),
        ("elevation-range", "What is the elevation range in the supplied DEM (metres)?", "elevation_range_m", 1.0),
        ("elevation-mean", "What is the mean elevation of valid DEM pixels (metres)?", "elevation_mean_m", 1.0),
        ("slope-mean", "What is the mean Horn 3x3 terrain slope (degrees)?", "slope_mean_degrees", 0.5),
        ("slope-max", "What is the maximum Horn 3x3 terrain slope (degrees)?", "slope_max_degrees", 0.5),
    ]
    return [
        {"id": f"tucson-{suffix}", "question": question, "answer": round(float(stats[key]), 4),
         "tolerance": tolerance, "source_metric": key}
        for suffix, question, key, tolerance in fields if stats.get(key) is not None
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dem", default="data/dem/tucson_srtm_utm12.tif")
    parser.add_argument("--output-dir", default="results/tucson")
    args = parser.parse_args()
    dem_path = Path(args.dem)
    if not dem_path.is_file():
        parser.error(f"DEM not found: {dem_path}. Download/project the raster locally first.")
    stats = analyze_dem(dem_path)
    questions = build_questions(stats)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "terrain_stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    (out / "questions.jsonl").write_text(
        "".join(json.dumps(q) + "\n" for q in questions), encoding="utf-8"
    )
    print(f"Analyzed {stats['valid_pixel_count']} valid DEM pixels")
    print(f"Elevation: {stats['elevation_min_m']:.1f}–{stats['elevation_max_m']:.1f} m")
    print(f"Mean slope: {stats['slope_mean_degrees']:.2f} degrees" if stats['slope_mean_degrees'] is not None else "Mean slope: unavailable")
    print(f"Wrote {len(questions)} reference questions to {out / 'questions.jsonl'}")
    print("No AI model was run. Supply actual model answers to src.evaluator for scoring.")


if __name__ == "__main__":
    main()
