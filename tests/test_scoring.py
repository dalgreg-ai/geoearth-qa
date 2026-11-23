import pytest
from src.benchmark import generate
from src.evaluator import score


def test_perfect_score():
    qs = generate()
    report = score(qs, [{'id': q['id'], 'answer': q['answer']} for q in qs])
    assert report['accuracy'] == 1
    assert report['total'] == 10


def test_missing_response_is_wrong():
    qs = generate()
    report = score(qs, [])
    assert report['correct'] == 0
    assert report['total'] == len(qs)


def test_duplicate_rejected():
    with pytest.raises(ValueError):
        score(generate(), [{'id': 'slope-01', 'answer': 1}, {'id': 'slope-01', 'answer': 2}])


def test_numeric_tolerance():
    q = [{'id': 'x', 'answer': 5.0, 'tolerance': 0.1}]
    assert score(q, [{'id': 'x', 'answer': '5.05'}])['correct'] == 1
    assert score(q, [{'id': 'x', 'answer': '5.2'}])['correct'] == 0
