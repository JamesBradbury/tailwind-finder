"""
Classes for weather forecast data. Might be turned into Django models at some point.
"""


class WeatherForecast:
    """
    Internal forecast object, independent of source data.
    """
    start_datetime = None
    end_datetime = None
    latitude = None
    longitude = None
    expected_wind_speed = None
    wind_direction_from = None
    pressure = None

    def __str__(self):
        print("#-#", self.start_datetime)
        start_str = self.start_datetime.strftime("%H%M %Y%m%d")
        return f"Forecast at: {start_str}, Wind: {self.expected_wind_speed} from: {self.wind_direction_from}"

    def __init__(self):
        pass

