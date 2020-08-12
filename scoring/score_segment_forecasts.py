"""
Package to provide scores for segments given their heading and a forecast.

Assumes that the forecast is relevant for the segment.
"""


def get_relative_heading(segment_heading, wind_direction):
    """
    Gives absolute degrees (0 - 180) between the segment heading and the wind direction.
    :param segment_heading: The compass heading of someone riding the segment.
    :param wind_direction: The heading from which the wind is *coming*. A wind from the North
    (Northerly) is 0.
    :return: Relative degrees between the two headings. 0 = exact headwind. 180 = exact tailwind.
    """
    if any(angle < 0 or angle > 360 for angle in [segment_heading, wind_direction]):
        raise ValueError(f"Headings and wind directions must be in the range 0-360. segment_heading: {segment_heading},"
                         f" wind_direction: {wind_direction}")
    abs_diff = abs(segment_heading - wind_direction)
    if abs_diff == 180:
        return 180
    return abs_diff % 180
