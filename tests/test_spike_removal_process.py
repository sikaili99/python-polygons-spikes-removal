import os

import pytest
from shapely import geometry

from utils import spike_process, spike_utils


@pytest.fixture
def simple_polygon_fixture():
    """
    Fixture for simple polygon, i.e., polygons without holes and a singular
    exterior boundary.
    """
    test_directory = os.path.abspath(os.path.dirname(__file__))
    test_data_path = os.path.join(
        test_directory,
        "test-data/test_simple_polygons_data.gpkg"
    )

    return spike_utils.load_geopackage(test_data_path)


@pytest.fixture
def polygon_with_holes():
    """
    Fixture for geometry with holes.
    """
    test_directory = os.path.abspath(os.path.dirname(__file__))
    test_data_path = os.path.join(
        test_directory,
        "test-data/test_spiky_polygons.gpkg"
    )

    return spike_utils.load_geopackage(test_data_path)


@pytest.fixture
def default_processor():
    """
    Fixture for the default GeometryProcessor
    """
    return spike_process.GeometryProcessor(1.0, 100000.0)


def test_polygon_without_spikes(simple_polygon_fixture, default_processor):
    """
    Test that the processing of a polygon without spikes returns the same
    polygon without any changes.
    """
    test_geom = (
        simple_polygon_fixture.loc[
            simple_polygon_fixture["name"] == "no_spikes"
        ]
        .geometry.values[0]
    )

    vertices = default_processor.process_sequence(
        spike_utils.extract_crs_geod(simple_polygon_fixture),
        test_geom.exterior.coords,
    )
    polygon = geometry.Polygon(vertices)

    assert polygon.equals(test_geom)


def test_polygon_multiple_spikes(simple_polygon_fixture, default_processor):
    """
    Test that a polygon with multiple spikes has all the spikes removed
    after processing.
    """
    test_geom = (
        simple_polygon_fixture.loc[
            simple_polygon_fixture["name"] == "multiple_spikes"
        ]
        .geometry.values[0]
    )

    vertices = default_processor.process_sequence(
        spike_utils.extract_crs_geod(simple_polygon_fixture),
        test_geom.exterior.coords,
    )
    polygon = geometry.Polygon(vertices)

    assert len(polygon.exterior.coords) == len(test_geom.exterior.coords) - 2


def test_polygon_single_criteria(simple_polygon_fixture, default_processor):
    """
    Test that a polygon with a spike that only meets one of the criteria
    used to mark spikes, is equal to the original polygon after processing.
    """
    test_geom = (
        simple_polygon_fixture.loc[
            simple_polygon_fixture["name"] == "single_criteria"
        ]
        .geometry.values[0]
    )

    vertices = default_processor.process_sequence(
        spike_utils.extract_crs_geod(simple_polygon_fixture),
        test_geom.exterior.coords,
    )
    polygon = geometry.Polygon(vertices)

    assert polygon.equals(test_geom)


def test_90_degree_angle():
    """Test that an angle is a 90 degree angle"""
    assert spike_process.get_angle_between_azimuths(0, 90) == 90


def test_0_degree_angle():
    """Test that an angle is a 0 degree angle"""
    assert spike_process.get_angle_between_azimuths(0, 0) == 0


def test_angle_is_wrapped():
    """Test that an angle is wrapped around the 180 degree angle"""
    assert spike_process.get_angle_between_azimuths(0, 270) == 90


def test_known_angle():
    """Test against a know angle"""
    assert spike_process.get_angle_between_azimuths(10, -15) == 25
