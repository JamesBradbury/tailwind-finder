"""
Classes for weather forecast data. Might be turned into Django models at some point.
"""


class WeatherForecast:
    """
    Internal forecast object, independent of source data.
    """

    def __str__(self):
        start_str = self.start_datetime.strftime("%H%M %Y%m%d")
        return f"Forecast at: {start_str}, Wind: {self.expected_wind_speed} from: {self.wind_direction_from}"

    def __init__(self, start_datetime, end_datetime, latitude, longitude, expected_wind_speed,
                 wind_direction_from, pressure):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.latitude = latitude
        self.longitude = longitude
        self.expected_wind_speed = expected_wind_speed
        self.wind_direction_from = wind_direction_from
        self.pressure = pressure
