import pytest
from src.terrain_analysis import slope_degrees, elevation_range, downslope_direction
from src.vegetation_analysis import ndvi, vegetated_fraction


def test_slope():
    assert slope_degrees(100, 100) == pytest.approx(45)


def test_invalid_run():
    with pytest.raises(ValueError):
        slope_degrees(10, 0)


def test_elevation_range():
    assert elevation_range([20, 30, 10]) == 20


def test_downslope():
    assert downslope_direction((0, 100), (100, 0)) == 'SE'


def test_ndvi():
    assert ndvi(0.6, 0.2) == pytest.approx(0.5)


def test_fraction():
    assert vegetated_fraction([0.1, 0.3, 0.4, 0.0]) == 0.5
