import pytest
from unittest.mock import patch, MagicMock
import http.client
# from _pytest import monkeypatch

import wind_forecasts.met_office

# https://docs.pytest.org/en/latest/monkeypatch.html
# https://stackoverflow.com/questions/55888381/python-mock-exception-http-client-response


class MockResponse:
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(http.client, "get", mock_get)


@pytest.fixture
def mock_connection(monkeypatch):
    """http.client HTTPSConnection mocked to return classes with some JSON"""
    class MockClient:
        def read(self, *args, **kwargs):
            return b'{"mock_key": "mock_response"}'

    class MockHTTPSConnection:
        def request(self, *args, **kwargs):
            return MockResponse

        def getresponse(self, *args, **kwargs):
            return MockClient()

    def mock_conn(*args, **kwargs):
        return MockHTTPSConnection()

    monkeypatch.setattr(http.client, "HTTPSConnection", mock_conn)


def test_get_met_office_json(mock_connection):
    mo_forecast_class = wind_forecasts.met_office.MetOfficeWeatherForecast()
    result = mo_forecast_class.get_met_office_json(1.111, 2.222)
    print("result:", result)
