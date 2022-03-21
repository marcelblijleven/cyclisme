import pytest

from django.contrib.auth.models import AnonymousUser
from cyclisme.apps.authenticate.models import User
from cyclisme.apps.strava.responses import AuthenticationResponse, AthleteResponse


@pytest.fixture()
def authenticated_user() -> User:
    # TODO: make fixture
    return User()


@pytest.fixture()
def anonymous_user() -> AnonymousUser:
    return AnonymousUser()


@pytest.fixture()
def authentication_response() -> AuthenticationResponse:
    athlete = AthleteResponse(
        "1337",
        "marcel",
        81.3,
        "https://test.nu/medium",
        "https://test.nu/",
    )
    response = AuthenticationResponse(
        "Bearer",
        1647811769,
        20000,
        "refresh_token",
        "access_token",
        athlete
    )

    return response
