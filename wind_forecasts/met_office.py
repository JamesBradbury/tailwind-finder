
import http.client
import json

from local_settings import METOFFICE_CLIENT_ID, METOFFICE_CLIENT_SECRET


def get_weather_forecast(lat, lon):
    conn = http.client.HTTPSConnection("api-metoffice.apiconnect.ibmcloud.com")

    headers = {
        'x-ibm-client-id': METOFFICE_CLIENT_ID,
        'x-ibm-client-secret': METOFFICE_CLIENT_SECRET,
        'accept': "application/json"
        }

    conn.request("GET",
                 f"/metoffice/production/v0/forecasts/point/three-hourly?latitude={lat}&longitude={lon}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    print("###", "2020-05-13T12:00Z" in data.decode("utf-8"))
    return json.loads(data.decode("utf-8"))


# Wind speed is in metres per second.
result = get_weather_forecast(lat=51.27987, lon=-2.77271)
print(type(result))
print(result["features"][0]["properties"]["timeSeries"])  # List of dicts

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

