"""Build a small deterministic, synthetic spatial reasoning benchmark."""
import json
from pathlib import Path
from .terrain_analysis import slope_degrees, elevation_range, downslope_direction
from .vegetation_analysis import ndvi, vegetated_fraction


def generate() -> list[dict]:
    items = []
    for i, (rise, run) in enumerate([(10, 100), (25, 200)], 1):
        items.append({'id': f'slope-{i:02}', 'domain': 'terrain', 'question': f'A site rises {rise} m over a horizontal distance of {run} m. What is its slope in degrees?', 'answer': round(slope_degrees(rise, run), 4), 'unit': 'degrees', 'tolerance': 0.1})
    for i, elevations in enumerate([[940, 956, 983], [1100, 1112, 1098]], 1):
        items.append({'id': f'relief-{i:02}', 'domain': 'terrain', 'question': f'What is the elevation range in meters for samples {elevations}?', 'answer': elevation_range(elevations), 'unit': 'm', 'tolerance': 0.01})
    for i, (nir, red) in enumerate([(0.6, 0.2), (0.35, 0.25)], 1):
        items.append({'id': f'ndvi-{i:02}', 'domain': 'vegetation', 'question': f'Compute NDVI for NIR={nir} and red={red}.', 'answer': round(ndvi(nir, red), 4), 'unit': 'unitless', 'tolerance': 0.01})
    for i, values in enumerate([[0.1, 0.3, 0.4, 0.0], [0.21, 0.19, 0.5, 0.6]], 1):
        items.append({'id': f'vegetation-{i:02}', 'domain': 'vegetation', 'question': f'What fraction of NDVI pixels {values} exceeds 0.2?', 'answer': vegetated_fraction(values), 'unit': 'fraction', 'tolerance': 0.001})
    items.append({'id': 'runoff-01', 'domain': 'hydrology', 'question': 'A 1000 m² site receives 0.025 m of rainfall with runoff coefficient 0.6. Estimate runoff volume in m³ using V=C×P×A.', 'answer': 15.0, 'unit': 'm3', 'tolerance': 0.01})
    items.append({'id': 'direction-01', 'domain': 'terrain', 'question': 'A high point has projected (east,north) coordinates (0,100) and a low point (100,0). What compass direction is downslope?', 'answer': downslope_direction((0,100), (100,0)), 'unit': 'compass', 'tolerance': 0})
    return items


def save(path: str | Path) -> None:
    Path(path).write_text(''.join(json.dumps(item) + '\n' for item in generate()), encoding='utf-8')


if __name__ == '__main__':
    save('data/sample_questions.jsonl')
