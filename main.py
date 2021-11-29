import click
from geopandas import GeoDataFrame
from shapely.geometry import Polygon
from utils import spike_process, spike_utils


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--angle", default=1.0, help="""
    Maximum angle, in degrees, used to evaluate spikes. Defaults to 1.0º.""")
@click.option("--distance", default=100000.0, help="""
    Minimum distance, in meters, used to evaluate spikes. Defaults to 100 000m
    """)
@click.option("-o", "--output", required=True, help="""
    Name of the output destination file""")
def main(filename: str, angle: float, distance: float, output: str):
    """
    A python command-line tool used to remove spikes from polygons stored in
    Geopackage format.
    """
    data = spike_utils.load_geopackage(filename)

    if not spike_utils.validate_crs(data):
        raise (
            """
            The input file doesn't have a valid coordinate seference
            system or it does not have a
            geographic coordinate seference system.
            """
        )

    geod = spike_utils.extract_crs_geod(data)
    processor = spike_process.GeometryProcessor(angle, distance)
    results = []

    for entry in data.itertuples():
        geometry = entry.geometry

        exterior = processor.process_sequence(geod, geometry.exterior.coords)

        interiors = []
        for interior_ring in geometry.interiors:
            processed_interior_ring = processor.process_sequence(
                geod,
                interior_ring.coords,
            )

            interiors.append(processed_interior_ring)

        results.append((entry.name, Polygon(exterior, interiors)))

    cleaned_data = GeoDataFrame(
        results,
        columns=["name", "geometry"],
        crs=data.crs
    )
    spike_utils.save_geopackage(output, cleaned_data)


if __name__ == '__main__':
    """""The main entery where the application is run from"""
    main()
