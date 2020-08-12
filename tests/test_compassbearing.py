import pytest
from stravalib.attributes import LatLon

from compassbearing import calculate_initial_compass_bearing


def test_directly_south_gives_180():
    start_latlong = tuple(LatLon(lat=51.27987, lon=-2.77271))
    end_latlong = tuple(LatLon(lat=51.27800, lon=-2.77271))
    assert calculate_initial_compass_bearing(
        point_a=start_latlong,
        point_b=end_latlong
    ) == pytest.approx(180.0, 0.01)


def test_directly_east_gives_90():
    start_latlong = tuple(LatLon(lat=51.27987, lon=-2.77271))
    end_latlong = tuple(LatLon(lat=51.27987, lon=-2.77200))
    assert calculate_initial_compass_bearing(
        point_a=start_latlong,
        point_b=end_latlong
    ) == pytest.approx(90.0, 0.01)


def test_directly_west_gives_270():
    start_latlong = tuple(LatLon(lat=51.27987, lon=-2.77271))
    end_latlong = tuple(LatLon(lat=51.27987, lon=-2.77300))
    assert calculate_initial_compass_bearing(
        point_a=start_latlong,
        point_b=end_latlong
    ) == pytest.approx(270.0, 0.01)


def test_directly_north_gives_0():
    start_latlong = tuple(LatLon(lat=51.27987, lon=-2.77300))
    end_latlong = tuple(LatLon(lat=51.28000, lon=-2.77300))
    assert calculate_initial_compass_bearing(
        point_a=start_latlong,
        point_b=end_latlong
    ) == pytest.approx(0.0, 0.01)


def test_directly_north_east_with_pos_lon_neg_lat():
    start_latlong = tuple(LatLon(lat=-22.5001, lon=33.0001))
    end_latlong = tuple(LatLon(lat=-22.5000, lon=33.00021))
    assert calculate_initial_compass_bearing(
        point_a=start_latlong,
        point_b=end_latlong
    ) == pytest.approx(45.0, 1)

