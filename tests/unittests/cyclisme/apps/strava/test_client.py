import pytest
import requests
from pytest_mock import MockFixture

from cyclisme.apps.strava.client import StravaClient, parse_authorization_response

response_data = {
    "token_type": "Bearer",
    "expires_at": 123456789,
    "expires_in": 12345,
    "refresh_token": "c0ff33refresh",
    "access_token": "c0ff33",
    "athlete": {
        "id": 1337,
        "username": "marcel",
        "weight": 81.3,
        "profile_medium": "https://test.nu/medium",
        "profile": "https://test.nu",
    }
}

missing_athlete_response_data = {
        "token_type": "Bearer",
        "expires_at": 123456789,
        "expires_in": 12345,
        "refresh_token": "c0ff33refresh",
        "access_token": "c0ff33",
    }


def test_parse_authorization_response():
    data = parse_authorization_response(response_data)
    assert data.token_type == response_data.get("token_type")
    assert data.expires_at == response_data.get("expires_at")
    assert data.expires_in == response_data.get("expires_in")
    assert data.access_token == response_data.get("access_token")
    assert data.refresh_token == response_data.get("refresh_token")
    assert data.athlete.id == response_data.get("athlete").get("id")
    assert data.athlete.username == response_data.get("athlete").get("username")
    assert data.athlete.weight == response_data.get("athlete").get("weight")
    assert data.athlete.profile_medium == response_data.get("athlete").get("profile_medium")
    assert data.athlete.profile == response_data.get("athlete").get("profile")


def test_parse_authorization_response_missing_athlete_raises():
    with pytest.raises(Exception) as e:
        _ = parse_authorization_response(missing_athlete_response_data)
        assert str(e.value) == "athlete is null"


def test_strava_client_authenticate(mocker: MockFixture, settings):
    mock_response = mocker.Mock()
    mock_post = mocker.patch("cyclisme.apps.strava.client.requests.post", return_value=mock_response)
    settings.STRAVA_CLIENT_ID = "1337"
    settings.STRAVA_CLIENT_SECRET = "tops3cret"

    StravaClient.authenticate("c0ff33")

    mock_post.assert_called_with(
        url="https://www.strava.com/oauth/token",
        params={'client_id': '1337',
                'client_secret': 'tops3cret',
                'code': 'c0ff33',
                'grant_type': 'authorization_code'}
    )
    mock_response.raise_for_status.assert_called_once()
