from pytest_mock import MockFixture

from cyclisme.apps.base.views.home import home


def test_home(mocker: MockFixture, rf, authenticated_user):
    request = rf.get("")
    request.user = authenticated_user

    mock_redirect = mocker.patch('cyclisme.apps.base.views.home.redirect')
    mock_render = mocker.patch('cyclisme.apps.base.views.home.render')

    _ = home(request)
    mock_redirect.assert_not_called()
    mock_render.assert_called_once_with(request, "home.html", context={})


def test_home_redirect_if_not_authenticated(mocker: MockFixture, rf, anonymous_user):
    request = rf.get("")
    request.user = anonymous_user

    mock_redirect = mocker.patch('cyclisme.apps.base.views.home.redirect')

    _ = home(request)
    mock_redirect.assert_called_once_with("login")

