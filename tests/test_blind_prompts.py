"""Blind prompt exports must not expose reference answers."""
from src.export_blind_prompts import blind_prompts


def test_blind_prompts_exclude_ground_truth():
    questions = [
        {"id": "tucson-elevation-min", "question": "Minimum?", "answer": 669,
         "tolerance": 1, "source_metric": "elevation_min_m"}
    ]
    assert blind_prompts(questions) == [
        {"id": "tucson-elevation-min", "question": "Minimum?"}
    ]
