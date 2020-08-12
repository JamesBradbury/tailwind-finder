import pytest

from scoring.score_segment_forecasts import get_relative_heading


class TestGetRelativeHeading:
    def test_both_north_returns_zero(self):
        assert get_relative_heading(
            segment_heading=0.0,
            wind_direction=0.0
        ) == 0

    def test_both_south_returns_zero(self):
        assert get_relative_heading(
            segment_heading=180.0,
            wind_direction=180.0
        ) == 0

    def test_north_south_returns_180(self):
        assert get_relative_heading(
            segment_heading=360.0,
            wind_direction=180.0
        ) == 180

    def test_east_and_west_returns_180(self):
        assert get_relative_heading(
            segment_heading=90.0,
            wind_direction=270.0
        ) == 180

    def test_north_and_west_returns_90(self):
        assert get_relative_heading(
            segment_heading=0.0,
            wind_direction=270.0
        ) == 90

    def test_west_and_south_returns_90(self):
        assert get_relative_heading(
            segment_heading=90.0,
            wind_direction=180.0
        ) == 90

    def test_nw_and_ne_returns_90(self):
        assert get_relative_heading(
            segment_heading=315.0,
            wind_direction=45.0
        ) == 90

    def test_bad_data_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            get_relative_heading(
                segment_heading=-20,
                wind_direction=10
            )
        assert str(exc_info.value) == \
            "Headings and wind directions must be in the range 0-360. " \
            "segment_heading: -20, wind_direction: 10"
