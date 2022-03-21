from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from cyclisme.apps.strava.responses import AuthenticationResponse


class UserAuthentication(models.Model):
    access_token = models.CharField(max_length=200, null=True)
    refresh_token = models.CharField(max_length=200, null=True)
    expires_in = models.IntegerField(null=True)
    expires_at = models.DateTimeField(null=True)
    # TODO: handle expiry


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    strava_id = models.CharField(max_length=200, unique=True)
    weight = models.FloatField(null=True)
    profile = models.URLField(null=True)
    profile_medium = models.URLField(null=True)
    authentication = models.OneToOneField(UserAuthentication, on_delete=models.DO_NOTHING, null=True)

    USERNAME_FIELD = 'strava_id'
    REQUIRED_FIELDS = []

    def create_or_update_authentication(self, authentication_response: AuthenticationResponse):
        """
        Sets the authentication information from the AuthenticationResponse to the user's authentication field
        :param self: the user to set the authentication data for
        :param authentication_response: the AuthenticationResponse with authentication data
        :return: None
        """
        if self.authentication is None:
            self.authentication = UserAuthentication.objects.create()

        self.authentication.access_token = authentication_response.access_token
        self.authentication.refresh_token = authentication_response.refresh_token
        self.authentication.expires_in = authentication_response.expires_in
        self.authentication.expires_at = datetime.fromtimestamp(authentication_response.expires_at)
        self.authentication.save()

    def __str__(self):
        return self.username
