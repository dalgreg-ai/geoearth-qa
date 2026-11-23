"""Simple remotely sensed vegetation indicators."""

def ndvi(nir: float, red: float) -> float:
    denominator = nir + red
    if denominator == 0:
        raise ValueError('NIR + red cannot be zero')
    return (nir - red) / denominator


def vegetated_fraction(ndvi_values: list[float], threshold: float = 0.2) -> float:
    if not ndvi_values:
        raise ValueError('NDVI values cannot be empty')
    return sum(v > threshold for v in ndvi_values) / len(ndvi_values)
