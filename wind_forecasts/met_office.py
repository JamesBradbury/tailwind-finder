import requests
from datetime import datetime, timedelta
from decimal import Decimal

from local_settings import METOFFICE_CLIENT_ID, METOFFICE_CLIENT_SECRET
from wind_forecasts.weather_model import WeatherForecast


class MetOfficeWeatherForecast(WeatherForecast):

    def get_met_office_json(self, lat, lon):
        url = "https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/three-hourly"
        params = dict(
            latitude=lat,
            longitude=lon
        )
        headers = {
            'x-ibm-client-id': METOFFICE_CLIENT_ID,
            'x-ibm-client-secret': METOFFICE_CLIENT_SECRET,
            'accept': "application/json"
        }

        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code != 200:
            raise ConnectionError(f"Unable to get data from Met Office, status: {response.status_code}")

        return response.json()

    @staticmethod
    def calculate_expected_wind_speed(wind_speed, gust_wind_speed):
        gust_weighting = Decimal("0.1")
        expected = Decimal(wind_speed) + Decimal(gust_wind_speed) * gust_weighting
        return expected

    def get_weather_forecast(self, lat, lon):
        forecast_length_hrs = 3
        forecasts_objects_list = []
        json_forecast = self.get_met_office_json(lat=lat, lon=lon)

        for forecast in json_forecast["features"][0]["properties"]["timeSeries"]:
            end_datetime = datetime.strptime(forecast["time"], "%Y-%m-%dT%H:%MZ")
            start_datetime = end_datetime - timedelta(hours=forecast_length_hrs)
            expected_wind_speed = MetOfficeWeatherForecast.calculate_expected_wind_speed(
                wind_speed=forecast["windSpeed10m"],
                gust_wind_speed=forecast["windGustSpeed10m"]
            )

            new_forecast = MetOfficeWeatherForecast()
            new_forecast.start_datetime = start_datetime
            new_forecast.end_datetime = end_datetime
            new_forecast.latitude = lat
            new_forecast.longitude = lon
            new_forecast.expected_wind_speed = Decimal(expected_wind_speed).quantize(Decimal("0.01"))
            new_forecast.wind_direction_from = int(forecast["windDirectionFrom10m"])
            new_forecast.pressure = int(forecast["mslp"])
        
            forecasts_objects_list.append(new_forecast)

        return forecasts_objects_list


met_office_forecast = MetOfficeWeatherForecast()
result = met_office_forecast.get_weather_forecast(lat=51.27987, lon=-2.77271)
print([str(f) for f in result])
print(len(result))


# For example:
#           {
#             "time": "2020-05-09T09:00Z",
#             "maxScreenAirTemp": 18.001032,
#             "minScreenAirTemp": 17.999784,
#             "max10mWindGust": 6.3982735,
#             "significantWeatherCode": 3,
#             "totalPrecipAmount": 0,
#             "totalSnowAmount": 0,
#             "windSpeed10m": 3.91,
#             "windDirectionFrom10m": 55,
#             "windGustSpeed10m": 6.17,
#             "visibility": 23220,
#             "mslp": 101340,
#             "screenRelativeHumidity": 68.69,
#             "feelsLikeTemp": 16.62,
#             "uvIndex": 4,
#             "probOfPrecipitation": 0,
#             "probOfSnow": 0,
#             "probOfHeavySnow": 0,
#             "probOfRain": 0,
#             "probOfHeavyRain": 0,
#             "probOfHail": 0,
#             "probOfSferics": 0
#           },

