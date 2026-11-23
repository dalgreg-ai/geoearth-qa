"""Tests for building real-data reference questions without requiring a DEM download."""
from src.tucson_demo import build_questions


def test_build_questions_from_metrics():
    metrics = {
        "elevation_min_m": 669.0, "elevation_max_m": 994.0,
        "elevation_range_m": 325.0, "elevation_mean_m": 754.3,
        "slope_mean_degrees": 2.34567, "slope_max_degrees": 19.0,
    }
    questions = build_questions(metrics)
    assert len(questions) == 6
    assert questions[2]["answer"] == 325.0
    assert questions[4]["answer"] == 2.3457
    assert questions[4]["tolerance"] == 0.5


def test_build_questions_skips_missing_slopes():
    metrics = {
        "elevation_min_m": 1, "elevation_max_m": 1,
        "elevation_range_m": 0, "elevation_mean_m": 1,
        "slope_mean_degrees": None, "slope_max_degrees": None,
    }
    assert len(build_questions(metrics)) == 4
