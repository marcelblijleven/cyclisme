from datetime import datetime

from requests.exceptions import HTTPError

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from cyclisme.apps.authenticate.models import User
from cyclisme.apps.strava.client import AuthenticationResponse, StravaClient
from cyclisme.apps.strava.utils import get_strava_uri, validate_scope


def authenticate_with_strava(code: str) -> AuthenticationResponse:
    """
    Helper method to call authenticate on the StravaClient
    :param code:
    :return:
    """
    return StravaClient.authenticate(code)


def login_view(request: HttpRequest) -> HttpResponse:
    """
    The view for the login page

    If a user is authenticated, it will render the home page
    :param request: WSGIRequest
    :return: HttpResponse
    """
    if request.user.is_authenticated:
        return render(request, "home.html", context={})

    return render(request, "login.html", context={})


def login_callback(request: HttpRequest) -> HttpResponse:
    """
    The callback URL which Strava uses.

    It will use the Strava Athlete ID to get or create a user from the database
    :param request: WSGIRequest
    :return: HttpResponse
    """
    code = request.GET.get("code")
    scope = request.GET.get("scope")

    if not validate_scope(scope):
        messages.error(request, "some required permissions are missing, please re-authenticate with Strava again")

        if request.user.is_authenticated:
            logout(request)

        return render(request, "login.html", {
            "scope_incomplete": True
        })

    try:
        authentication_response = authenticate_with_strava(code)
    except HTTPError as e:
        return HttpResponse(f"exception occurred during authentication: {e}", status=500)

    if authentication_response.access_token is None:
        # TODO: log error, alert user and redirect to home
        return HttpResponse("did not receive access token", status=500)

    if (athlete := authentication_response.athlete) is None:
        # TODO: log error, alert user and redirect to home
        return HttpResponse("did not receive athlete in authentication response", status=500)

    if (user := authenticate(strava_id=athlete.id)) is None:
        # No user exists for this strava athlete, so we create one
        user = User.objects.create(strava_id=athlete.id)
        user.username = athlete.username
        user.weight = athlete.weight
        user.profile_medium = athlete.profile_medium
        user.profile = athlete.profile
        user.save()

    user.create_or_update_authentication(authentication_response)
    login(request, user)

    messages.success(request, f"successfully logged in as {user}")
    return redirect("home")


def login_redirect(request: HttpRequest) -> HttpResponse:
    """
    Redirects the user to the Strava authorization page
    :param request: HttpRequest
    :return: HttpResponse
    """
    strava_uri = get_strava_uri()
    return redirect(strava_uri)
