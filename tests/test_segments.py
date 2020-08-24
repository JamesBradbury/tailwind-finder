import pytest

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

