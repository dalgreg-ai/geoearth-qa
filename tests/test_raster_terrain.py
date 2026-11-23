"""Analytical checks for the local GeoTIFF terrain analyzer."""
import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin

from src.raster_terrain import analyze_dem


def write_dem(tmp_path, data, *, crs='EPSG:32612', nodata=None):
    path = tmp_path / 'test_dem.tif'
    with rasterio.open(
        path, 'w', driver='GTiff', height=data.shape[0], width=data.shape[1],
        count=1, dtype='float32', crs=crs,
        transform=from_origin(500000, 3600000, 10, 10), nodata=nodata,
    ) as dst:
        dst.write(data.astype('float32'), 1)
    return path


def test_flat_dem(tmp_path):
    result = analyze_dem(write_dem(tmp_path, np.full((5, 5), 100.0)))
    assert result['valid_pixel_count'] == 25
    assert result['terrain_pixel_count'] == 9
    assert result['elevation_range_m'] == 0
    assert result['slope_mean_degrees'] == pytest.approx(0)
    assert result['aspect_mean_degrees'] is None


def test_east_downslope(tmp_path):
    # Elevation falls 10 metres per 10-metre pixel towards the east.
    data = 100 - 10 * np.arange(5)[None, :] + np.zeros((5, 1))
    result = analyze_dem(write_dem(tmp_path, data))
    assert result['slope_mean_degrees'] == pytest.approx(45)
    assert result['slope_max_degrees'] == pytest.approx(45)
    assert result['aspect_mean_degrees'] == pytest.approx(90)


def test_north_downslope(tmp_path):
    # Elevation rises towards the south, so downslope is north.
    data = 100 + 10 * np.arange(5)[:, None] + np.zeros((1, 5))
    result = analyze_dem(write_dem(tmp_path, data))
    assert result['slope_mean_degrees'] == pytest.approx(45)
    assert result['aspect_mean_degrees'] == pytest.approx(0)


def test_nodata_excludes_neighborhoods(tmp_path):
    data = np.full((5, 5), 100.0)
    data[2, 2] = -9999
    result = analyze_dem(write_dem(tmp_path, data, nodata=-9999))
    assert result['valid_pixel_count'] == 24
    assert result['terrain_pixel_count'] == 0
    assert result['slope_mean_degrees'] is None


def test_geographic_crs_rejected(tmp_path):
    path = write_dem(tmp_path, np.ones((5, 5)), crs='EPSG:4326')
    with pytest.raises(ValueError, match='projected CRS'):
        analyze_dem(path)
