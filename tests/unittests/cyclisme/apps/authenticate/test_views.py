import copy

import pytest
from django.http import HttpResponse
from pytest_mock import MockFixture

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from requests import HTTPError

from cyclisme.apps.authenticate.models import User
from cyclisme.apps.authenticate.views import authenticate_with_strava, login_view, login_callback


def test_authenticate_with_strava(mocker: MockFixture):
    mock_strava_client = mocker.patch("cyclisme.apps.authenticate.views.StravaClient")
    _ = authenticate_with_strava("auth_code")
    mock_strava_client.authenticate.assert_called_with("auth_code")


def test_login_view_authenticated(rf, mocker: MockFixture):
    request = rf.request()
    request.user = User()
    mock_render = mocker.patch("cyclisme.apps.authenticate.views.render")

    login_view(request)

    mock_render.assert_called_with(request, "home.html", context={})


def test_login_view_anonymous(rf, mocker: MockFixture):
    request = rf.request()
    mock_render = mocker.patch("cyclisme.apps.authenticate.views.render")
    request.user = AnonymousUser()
    login_view(request)

    mock_render.assert_called_with(request, "login.html", context={})


@pytest.mark.django_db
def test_login_callback(rf, mocker: MockFixture, authentication_response):
    mock_authenticate_with_strava = mocker.patch(
        "cyclisme.apps.authenticate.views.authenticate_with_strava",
        return_value=authentication_response,
    )
    mock_render = mocker.patch("cyclisme.apps.authenticate.views.render")
    mock_redirect = mocker.patch("cyclisme.apps.authenticate.views.redirect")
    mock_messages = mocker.patch("cyclisme.apps.authenticate.views.messages")

    request = rf.get("/login_callback?code=c0ff33&scope=read,read_all,profile:read_all,activity:read_all")
    # set session middleware
    get_response = mocker.MagicMock()
    middleware = SessionMiddleware(get_response)
    middleware.process_request(request)
    request.session.save()

    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    login_callback(request)

    mock_authenticate_with_strava.assert_called_with("c0ff33")
    mock_render.assert_not_called()
    mock_redirect.assert_called_with("home")
    mock_messages.success.assert_called_once_with(request, "successfully logged in as marcel")


@pytest.mark.django_db
def test_login_callback_existing_user(rf, mocker: MockFixture, authentication_response):
    mock_authenticate_with_strava = mocker.patch(
        "cyclisme.apps.authenticate.views.authenticate_with_strava",
        return_value=authentication_response,
    )
    mock_render = mocker.patch("cyclisme.apps.authenticate.views.render")
    mock_redirect = mocker.patch("cyclisme.apps.authenticate.views.redirect")
    mock_messages = mocker.patch("cyclisme.apps.authenticate.views.messages")

    request = rf.get("/login_callback?code=c0ff33&scope=read,read_all,profile:read_all,activity:read_all")
    # set session middleware
    get_response = mocker.MagicMock()
    middleware = SessionMiddleware(get_response)
    middleware.process_request(request)
    request.session.save()

    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    user = User.objects.create(strava_id="1337")
    user.username = "test user marcel"
    user.save()

    login_callback(request)

    mock_authenticate_with_strava.assert_called_with("c0ff33")
    mock_render.assert_not_called()
    mock_redirect.assert_called_with("home")
    mock_messages.success.assert_called_once_with(request, "successfully logged in as test user marcel")


def test_login_callback_invalid_scope(rf, mocker: MockFixture, authentication_response, anonymous_user):
    mock_render = mocker.patch("cyclisme.apps.authenticate.views.render")
    mock_messages = mocker.patch(
        "cyclisme.apps.authenticate.views.messages"
    )

    request = rf.get("/login_callback?code=c0ff33&scope=read")
    request.user = anonymous_user
    login_callback(request)

    mock_messages.error.assert_called_with(
        request,
        "some required permissions are missing, please re-authenticate with Strava again",
    )
    mock_render.assert_called_with(request, "login.html", {"scope_incomplete": True})


def test_login_callback_invalid_scope_with_authenticated_user(rf, mocker: MockFixture, authenticated_user):
    mock_render = mocker.patch("cyclisme.apps.authenticate.views.render")
    mock_messages = mocker.patch(
        "cyclisme.apps.authenticate.views.messages"
    )
    mock_logout = mocker.patch(
        "cyclisme.apps.authenticate.views.logout"
    )

    request = rf.get("/login_callback?code=c0ff33&scope=read")
    request.user = authenticated_user
    login_callback(request)

    mock_messages.error.assert_called_with(
        request,
        "some required permissions are missing, please re-authenticate with Strava again",
    )
    mock_logout.assert_called_with(request)
    mock_render.assert_called_with(request, "login.html", {"scope_incomplete": True})


def test_login_callback_authenticate_raises(rf, mocker: MockFixture):
    mock_authenticate_with_strava = mocker.patch(
        "cyclisme.apps.authenticate.views.authenticate_with_strava",
        side_effect=HTTPError("invalid access token"),
    )

    request = rf.get("/login_callback?code=c0ff33&scope=read,read_all,profile:read_all,activity:read_all")
    response = login_callback(request)
    mock_authenticate_with_strava.assert_called_with("c0ff33")
    expected_response = HttpResponse(f"exception occurred during authentication: invalid access token", status=500)
    assert expected_response.getvalue() == response.getvalue()


def test_login_callback_access_token_is_none(rf, mocker: MockFixture, authentication_response):
    no_access_token_response = copy.deepcopy(authentication_response)
    no_access_token_response.access_token = None
    mock_authenticate_with_strava = mocker.patch(
        "cyclisme.apps.authenticate.views.authenticate_with_strava",
        return_value=no_access_token_response,
    )

    request = rf.get("/login_callback?code=c0ff33&scope=read,read_all,profile:read_all,activity:read_all")
    response = login_callback(request)
    expected_response = HttpResponse(f"did not receive access token", status=500)
    assert expected_response.getvalue() == response.getvalue()
    mock_authenticate_with_strava.assert_called_with("c0ff33")
