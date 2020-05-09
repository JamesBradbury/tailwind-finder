"""
Classes for weather forecast data. Might be turned into Django models at some point.
"""


class WeatherForecast:

    def __init__(self, start_datetime, end_datetime, latitude, longitude, expected_wind_speed,
                 wind_direction_from):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.latitude = latitude
        self.longitude = longitude
        self.expected_wind_speed = expected_wind_speed
        self.wind_direction_from = wind_direction_from
