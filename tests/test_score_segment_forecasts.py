from datetime import datetime

import pytest

from scoring.score_segment_forecasts import get_relative_heading, score_segment_from_forecast, get_wind_angle_effect
from wind_forecasts.weather_model import WeatherForecast


class TestGetRelativeHeading:
    def test_both_north_returns_zero(self):
        assert get_relative_heading(
            segment_bearing=0.0,
            wind_direction=0.0
        ) == 0

    def test_both_south_returns_zero(self):
        assert get_relative_heading(
            segment_bearing=180.0,
            wind_direction=180.0
        ) == 0

    def test_north_south_returns_180(self):
        assert get_relative_heading(
            segment_bearing=360.0,
            wind_direction=180.0
        ) == 180

    def test_east_and_west_returns_180(self):
        assert get_relative_heading(
            segment_bearing=90.0,
            wind_direction=270.0
        ) == 180

    def test_north_and_west_returns_90(self):
        assert get_relative_heading(
            segment_bearing=0.0,
            wind_direction=270.0
        ) == 90

    def test_west_and_south_returns_90(self):
        assert get_relative_heading(
            segment_bearing=90.0,
            wind_direction=180.0
        ) == 90

    def test_nw_and_ne_returns_90(self):
        assert get_relative_heading(
            segment_bearing=315.0,
            wind_direction=45.0
        ) == 90

    def test_100_99_return_1(self):
        assert get_relative_heading(
            segment_bearing=100.0,
            wind_direction=99.0
        ) == 1

    def test_bad_data_raises_value_error(self):
        with pytest.raises(ValueError) as exc_info:
            get_relative_heading(
                segment_bearing=-20,
                wind_direction=10
            )
        assert str(exc_info.value) == \
            "Headings and wind directions must be in the range 0-360. " \
            "segment_bearing: -20, wind_direction: 10"


class TestScoreSegmentFromForecast:
    date_example = datetime.strptime("2020-01-01T10:00Z", "%Y-%m-%dT%H:%MZ")

    def test_no_wind_returns_zero(self):
        forecast = WeatherForecast()
        forecast.start_datetime = self.date_example
        forecast.wind_direction_from = 10.0
        forecast.expected_wind_speed = 0.0
        assert score_segment_from_forecast(segment=dict(bearing=100.0), forecast=forecast) == 0

    def test_near_headwind_returns_negative_score(self):
        forecast = WeatherForecast()
        forecast.start_datetime = self.date_example
        forecast.wind_direction_from = 99.0
        forecast.expected_wind_speed = 10.0
        assert score_segment_from_forecast(segment=dict(bearing=100.0), forecast=forecast) < 0

    def test_exact_tailwind_gives_higher_score_than_almost_tailwind(self):
        forecast = WeatherForecast()
        forecast.start_datetime = self.date_example
        forecast.wind_direction_from = 190.0
        forecast.expected_wind_speed = 15.0
        exact_tailwind_score = score_segment_from_forecast(segment=dict(bearing=10), forecast=forecast)
        near_tailwind_score = score_segment_from_forecast(segment=dict(bearing=11), forecast=forecast)
        assert exact_tailwind_score > near_tailwind_score

    def test_exact_headwind_gives_lower_score_than_almost_headwind(self):
        forecast = WeatherForecast()
        forecast.start_datetime = self.date_example
        forecast.wind_direction_from = 50.0
        forecast.expected_wind_speed = 15.0
        exact_headwind_score = score_segment_from_forecast(segment=dict(bearing=50), forecast=forecast)
        near_headwind_score = score_segment_from_forecast(segment=dict(bearing=49), forecast=forecast)
        assert exact_headwind_score < near_headwind_score

    def test_other_scores(self):
        forecast = WeatherForecast()
        forecast.start_datetime = self.date_example
        forecast.wind_direction_from = 0.0
        forecast.expected_wind_speed = 10.0


class TestGetWindAngleEffect:
    def test_various(self):
        for a in range(0, 180, 10):
            print(a, get_wind_angle_effect(a))

        pass
