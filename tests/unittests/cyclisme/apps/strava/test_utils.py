from cyclisme.apps.strava.utils import get_strava_uri, validate_scope


def test_get_strava_uri(settings):
    settings.STRAVA_CLIENT_ID = 1337
    settings.STRAVA_SCOPE = "read_all,profile:read_all,activity:read_all"
    settings.STRAVA_CALLBACK_URI = "https://callback.uri"

    strava_uri = get_strava_uri()
    assert strava_uri == "https://www.strava.com/oauth/authorize" \
                         "?client_id=1337" \
                         "&response_type=code" \
                         "&redirect_uri=https://callback.uri" \
                         "&approval_prompt=force" \
                         "&scope=read_all,profile:read_all,activity:read_all"


def test_validate_scope():
    assert validate_scope("read,read_all,profile:read_all,activity:read_all")
    assert validate_scope("read,activity:read_all,profile:read_all,read_all")

    assert not validate_scope("read_all,profile:read_all")
    assert not validate_scope("read_all,activity:read_all")
    assert not validate_scope("profile:read_all,activity:read_all")
    assert not validate_scope("")
