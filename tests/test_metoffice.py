import pytest
from pytest_mock import mocker
import wind_forecasts.met_office
from local_settings import METOFFICE_CLIENT_SECRET, METOFFICE_CLIENT_ID


def mock_requests_get():
    return b'{"mock_key1": "mock_response1"}'


def test_get_met_office_json_200(mocker):
    """Method calls requests.get with the right lat-lon values."""
    mocked_get = mocker.patch('wind_forecasts.met_office.requests.get')
    mocked_get.return_value = mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json = mock_requests_get
    mo_forecast_class = wind_forecasts.met_office.MetOfficeWeatherForecast()
    mo_forecast_class.get_met_office_json(1.111, 2.222, url="httpx://notreal.com")
    mocked_get.assert_called_with(
        url='httpx://notreal.com',
        headers={'x-ibm-client-id': METOFFICE_CLIENT_ID,
                 'x-ibm-client-secret': METOFFICE_CLIENT_SECRET,
                 'accept': 'application/json'}, params={'latitude': 1.111, 'longitude': 2.222})


def test_get_met_office_json_404(mocker):
    """Getting a 404 from API will raise a ConnectionError."""
    mocked_get = mocker.patch('wind_forecasts.met_office.requests.get')
    mocked_get.return_value = mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.json = mock_requests_get
    mo_forecast_class = wind_forecasts.met_office.MetOfficeWeatherForecast()

    with pytest.raises(ConnectionError):
        mo_forecast_class.get_met_office_json(1.111, 2.222, url="httpx://notreal.com")


