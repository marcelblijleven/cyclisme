from django.conf import settings


def get_strava_uri() -> str:
    client_id = settings.STRAVA_CLIENT_ID
    scope = settings.STRAVA_SCOPE
    callback_uri = settings.STRAVA_CALLBACK_URI
    strava_uri = f"https://www.strava.com/oauth/authorize" \
                 f"?client_id={client_id}" \
                 f"&response_type=code" \
                 f"&redirect_uri={callback_uri}" \
                 f"&approval_prompt=force" \
                 f"&scope={scope}"

    return strava_uri


def validate_scope(scope: str) -> bool:
    expected_scope = ["read", "read_all", "profile:read_all", "activity:read_all"]
    parsed_scope = scope.split(",")
    return sorted(expected_scope) == sorted(parsed_scope)
