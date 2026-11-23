"""Pure Python terrain calculations, independent of Earth Engine."""
import math


def slope_degrees(rise_m: float, run_m: float) -> float:
    if run_m <= 0:
        raise ValueError('Horizontal run must be positive')
    return math.degrees(math.atan(abs(rise_m) / run_m))


def elevation_range(elevations_m: list[float]) -> float:
    if not elevations_m:
        raise ValueError('Elevations cannot be empty')
    return max(elevations_m) - min(elevations_m)


def downslope_direction(high: tuple[float, float], low: tuple[float, float]) -> str:
    """Cardinal direction from high to low using projected east/north coordinates."""
    dx, dy = low[0] - high[0], low[1] - high[1]
    if dx == dy == 0:
        raise ValueError('Points must differ')
    angle = math.degrees(math.atan2(dx, dy)) % 360
    return ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')[int((angle + 22.5) // 45) % 8]
