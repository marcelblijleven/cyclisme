from typing import Any

import requests

from django.conf import settings

from cyclisme.apps.strava.responses import AthleteResponse, AuthenticationResponse


def parse_authorization_response(response_data) -> AuthenticationResponse:
    athlete_data = response_data.get("athlete")

    if athlete_data is None:
        raise Exception("athlete is null")

    athlete = AthleteResponse(
        id=athlete_data.get("id"),
        username=athlete_data.get("username"),
        weight=athlete_data.get("weight"),
        profile_medium=athlete_data.get("profile_medium"),
        profile=athlete_data.get("profile"),
    )

    auth_response = AuthenticationResponse(
        token_type=response_data.get("token_type"),
        expires_at=response_data.get("expires_at"),
        expires_in=response_data.get("expires_in"),
        refresh_token=response_data.get("refresh_token"),
        access_token=response_data.get("access_token"),
        athlete=athlete,
    )
    return auth_response


class StravaClient:
    @staticmethod
    def authenticate(code: str) -> AuthenticationResponse:
        """

        :param code:
        :return:
        """
        token_url = "https://www.strava.com/oauth/token"
        params = {
            "client_id": settings.STRAVA_CLIENT_ID,
            "client_secret": settings.STRAVA_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
        }

        res = requests.post(url=token_url, params=params)
        res.raise_for_status()
        return parse_authorization_response(res.json())
