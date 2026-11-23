"""Optional live Google Earth Engine example. Requires an approved EE account/project.

No imagery is redistributed. The chosen site is an illustrative Tucson-area rectangle.
This is a separate optional workflow, not required for benchmark tests.
"""
import argparse


def summarize(project: str):
    try:
        import ee
    except ImportError as exc:
        raise RuntimeError('Install earthengine-api first: pip install -r requirements-earthengine.txt') from exc
    ee.Initialize(project=project)
    region = ee.Geometry.Rectangle([-110.98, 32.20, -110.97, 32.21])
    dem = ee.Image('USGS/SRTMGL1_003').select('elevation')
    terrain = ee.Terrain.slope(dem)
    stats = terrain.reduceRegion(reducer=ee.Reducer.mean(), geometry=region, scale=30, maxPixels=1_000_000).getInfo()
    return {'study_area': 'illustrative Tucson rectangle', 'mean_slope_degrees': stats.get('slope'), 'source': 'USGS/SRTMGL1_003', 'method': 'ee.Terrain.slope, mean at 30 m scale'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True, help='Your Google Cloud project with Earth Engine enabled')
    args = parser.parse_args()
    print(summarize(args.project))
