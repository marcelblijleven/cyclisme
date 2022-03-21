from cyclisme.apps.strava.responses import AthleteResponse, AuthenticationResponse


def test_athlete_response__str__():
    athlete = AthleteResponse(
        id="abc",
        username="marcel",
        weight=81.3,
        profile_medium="https://test.nl/medium",
        profile="https://test.nl",
    )

    assert str(athlete) == athlete.username
