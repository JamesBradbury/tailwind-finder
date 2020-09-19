import pytest
from stravalib.attributes import LatLon
from stravalib.model import Segment

import segments


def test_get_clean_segment_id_int_in_string():
    assert segments.UserSegment.get_clean_segment_id(
        segment={"id": "123456"}
    ) == 123456


def test_get_clean_segment_id_url():
    assert segments.UserSegment.get_clean_segment_id(
        segment={"id": "https://www.strava.com/segments/123456"}
    ) == 123456


def test_get_clean_segment_id_bad_url():
    with pytest.raises(ValueError) as exc_info:
        segments.UserSegment.get_clean_segment_id(
            segment={"id": "https://www.strava.com/segments123456"}
        )
    assert str(exc_info.value) == "Invalid Segment URL https://www.strava.com/segments123456. Must end with an integer."


def test_user_segment_from_stravalib_segment_object():
    seg_obj = Segment(
        id=12345,
        name="test_name",
        start_latlng=LatLon(lat=51.416433, lon=-2.247566),
        end_latlng=LatLon(lat=51.420233, lon=-2.240333)
    )
    new_user_seg = segments.UserSegment.from_stravalib_segment_object(segment_obj=seg_obj)
    assert new_user_seg.strava_id == 12345
    assert new_user_seg.name_str == "test_name"
    assert new_user_seg.start_latlng == LatLon(lat=51.416433, lon=-2.247566)
    assert new_user_seg.end_latlng == LatLon(lat=51.420233, lon=-2.240333)
    assert new_user_seg.bearing == 49.88507827763817

# TODO: Test SegmentsArchive
