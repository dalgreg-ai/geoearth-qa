"""Local terrain analysis for single-band elevation GeoTIFFs.

Distances and elevations must be in metres. Reproject geographic rasters to an
appropriate projected CRS before computing slope or aspect.
"""
from pathlib import Path
import numpy as np
import rasterio


def analyze_dem(path: str | Path) -> dict:
    """Return elevation, slope and aspect summaries for a projected DEM.

    Slope and aspect are calculated on interior cells with complete 3x3 valid
    neighborhoods. Aspect is clockwise from north, indicating downslope direction.
    """
    with rasterio.open(path) as ds:
        if ds.count != 1:
            raise ValueError("Expected a single-band elevation raster")
        if ds.crs is None or not ds.crs.is_projected:
            raise ValueError("DEM must use a projected CRS with metre units")
        if abs(ds.crs.linear_units_factor[1] - 1.0) > 1e-9:
            raise ValueError("DEM projected CRS must use metre units")
        if abs(ds.transform.b) > 1e-10 or abs(ds.transform.d) > 1e-10:
            raise ValueError("Rotated rasters are not supported")
        dx, dy = abs(ds.transform.a), abs(ds.transform.e)
        if dx <= 0 or dy <= 0:
            raise ValueError("Pixel dimensions must be positive")
        dem = ds.read(1, masked=True).astype(np.float64)

    valid = ~np.ma.getmaskarray(dem) & np.isfinite(dem.data)
    if not valid.any():
        raise ValueError("DEM contains no valid elevation pixels")
    elevations = dem.data[valid]
    result = {
        "valid_pixel_count": int(valid.sum()),
        "elevation_min_m": float(elevations.min()),
        "elevation_max_m": float(elevations.max()),
        "elevation_mean_m": float(elevations.mean()),
        "elevation_range_m": float(np.ptp(elevations)),
        "slope_mean_degrees": None,
        "slope_max_degrees": None,
        "aspect_mean_degrees": None,
        "terrain_pixel_count": 0,
    }
    if min(dem.shape) < 3:
        return result

    z = dem.data
    neighborhood_valid = valid[1:-1, 1:-1].copy()
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            neighborhood_valid &= valid[1+i:z.shape[0]-1+i, 1+j:z.shape[1]-1+j]

    # Horn's 3x3 finite differences; north-up GeoTIFF rows increase southward.
    dzdx = ((z[:-2, 2:] + 2*z[1:-1, 2:] + z[2:, 2:])
            - (z[:-2, :-2] + 2*z[1:-1, :-2] + z[2:, :-2])) / (8*dx)
    dzdy_south = ((z[2:, :-2] + 2*z[2:, 1:-1] + z[2:, 2:])
                  - (z[:-2, :-2] + 2*z[:-2, 1:-1] + z[:-2, 2:])) / (8*dy)
    magnitude = np.hypot(dzdx, dzdy_south)
    slopes = np.degrees(np.arctan(magnitude))
    terrain_valid = neighborhood_valid & (magnitude > 1e-12)
    all_slopes = slopes[neighborhood_valid]
    if all_slopes.size:
        result["slope_mean_degrees"] = float(all_slopes.mean())
        result["slope_max_degrees"] = float(all_slopes.max())
        result["terrain_pixel_count"] = int(all_slopes.size)
    if terrain_valid.any():
        # Clockwise from north: east component=-dzdx, north component=dzdy_south.
        aspects = (np.degrees(np.arctan2(-dzdx[terrain_valid], dzdy_south[terrain_valid])) + 360) % 360
        radians = np.radians(aspects)
        mean_sin, mean_cos = np.sin(radians).mean(), np.cos(radians).mean()
        if np.hypot(mean_sin, mean_cos) > 1e-12:
            result["aspect_mean_degrees"] = float(np.degrees(np.arctan2(mean_sin, mean_cos)) % 360)
    return result
