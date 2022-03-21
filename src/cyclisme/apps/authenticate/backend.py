from typing import Optional

from django.contrib.auth.backends import ModelBackend

from cyclisme.apps.authenticate.models import User


class AuthBackend(ModelBackend):
    """
    Log into Django using only the strava id
    """

    def authenticate(self, request, strava_id=None, password=None, **kwargs) -> Optional[User]:
        try:
            return User.objects.get(strava_id=strava_id)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
