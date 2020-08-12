"""
Package to provide scores for segments given their heading and a forecast.

Assumes that the forecast is relevant for the segment.
"""
from math import sin
from typing import Dict, Union

from wind_forecasts.weather_model import WeatherForecast


def get_relative_heading(segment_bearing: Union[int, float], wind_direction: Union[int, float]) -> float:
    """
    Gives absolute degrees (0 - 180) between the segment bearing and the wind direction.
    :param segment_bearing: The compass heading of someone riding the segment.
    :param wind_direction: The heading from which the wind is *coming*. A wind from the North
    (Northerly) is 0.
    :return: Relative degrees between the two headings. 0 = exact headwind. 180 = exact tailwind.
    """
    if any(angle < 0 or angle > 360 for angle in [segment_bearing, wind_direction]):
        raise ValueError(f"Headings and wind directions must be in the range 0-360. segment_bearing: {segment_bearing},"
                         f" wind_direction: {wind_direction}")
    abs_diff = abs(segment_bearing - wind_direction)
    if abs_diff == 180:
        return 180
    return abs_diff % 180


def get_wind_angle_effect(relative_heading):
    return ((sin((relative_heading * 0.0434) / 2.49)) * 25) - 7


def score_segment_from_forecast(segment: Dict, forecast: WeatherForecast) -> int:
    """
    Gives a integer score, positive or negative depending on wind speed and direction relative
    to the segment bearing.
    Based loosely on these graphs: https://www.sheldonbrown.com/brandt/wind.html
    :param segment: Dictionary with the key bearing storing a float
    :param forecast: Forecast object with wind direction and wind speed
    :return: Score showing how much hindrance/assistance the wind will provide at that forecast time.
    0=no difference.
    """
    if forecast.expected_wind_speed == 0:
        return 0
    relative_heading = get_relative_heading(segment_bearing=segment["bearing"],
                                            wind_direction=forecast.wind_direction_from)
    print("### relative_heading", relative_heading)
    # Calcated to mirror the effect described in the link above.
    # ( sin( (0.0434 * x - 176) / 2.49) * 25 ) - 7
    wind_angle_effect = get_wind_angle_effect(relative_heading=relative_heading)
    score = wind_angle_effect * forecast.expected_wind_speed

    return score
