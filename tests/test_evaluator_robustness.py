"""Evaluator safety and accounting tests."""
import math
import pytest
from src.evaluator import score


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf"), "NaN", "Infinity", None])
def test_nonfinite_or_missing_numeric_answer_is_wrong(bad):
    q = [{"id": "a", "answer": 10.0, "tolerance": 0.5}]
    assert score(q, [{"id": "a", "answer": bad}])["correct"] == 0


def test_duplicate_reference_question_rejected():
    q = [{"id": "a", "answer": 1}, {"id": "a", "answer": 2}]
    with pytest.raises(ValueError, match="Duplicate question IDs"):
        score(q, [])


def test_missing_response_counted_wrong():
    q = [{"id": "a", "answer": 1}, {"id": "b", "answer": 2}]
    result = score(q, [{"id": "a", "answer": 1}])
    assert (result["total"], result["correct"], result["accuracy"]) == (2, 1, 0.5)
