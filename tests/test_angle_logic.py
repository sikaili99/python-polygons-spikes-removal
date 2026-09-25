"""
Unit tests for the pure geometric logic in ``utils.spike_process`` that does
not depend on geopandas / GeoPackage fixtures. These exercise the angle helper
and the sequence-processing guard rails directly.
"""
import pyproj
import pytest

from utils import spike_process


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 90, 90),
        (0, 0, 0),
        (0, 270, 90),   # wraps around 180
        (10, -15, 25),
        (350, 10, 20),   # wraps across 0/360
        (180, 0, 180),
    ],
)
def test_angle_between_azimuths(a, b, expected):
    assert spike_process.get_angle_between_azimuths(a, b) == expected


def test_angle_is_symmetric():
    assert spike_process.get_angle_between_azimuths(
        30, 200
    ) == spike_process.get_angle_between_azimuths(200, 30)


def test_processor_normalizes_constructor_args():
    """min_angle is wrapped mod 360 and min_distance is made non-negative."""
    processor = spike_process.GeometryProcessor(365.0, -50.0)
    assert processor.min_angle == 5.0
    assert processor.min_distance == 50.0


def test_short_sequence_is_returned_unchanged():
    """
    A ring with 4 or fewer coordinates is a triangle (closed ring) and must be
    returned untouched to avoid producing an invalid polygon.
    """
    processor = spike_process.GeometryProcessor(1.0, 100000.0)
    geod = pyproj.Geod(ellps="WGS84")
    triangle = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 0.0)]
    assert processor.process_sequence(geod, triangle) == triangle


def test_triplet_below_distance_is_never_a_spike():
    """
    If both boundary edges of the triplet are shorter than min_distance, the
    triplet is not evaluated as a spike regardless of its angle.
    """
    processor = spike_process.GeometryProcessor(1.0, 100000.0)
    geod = pyproj.Geod(ellps="WGS84")
    # Three points a few metres apart -> distances well below 100 km.
    triplet = [(0.0, 0.0), (0.00001, 0.0), (0.00002, 0.0)]
    assert processor.process_triplet(geod, triplet) is False
