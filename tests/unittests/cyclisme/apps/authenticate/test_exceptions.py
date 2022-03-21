from cyclisme.apps.authenticate.exceptions import AuthenticationException


def test_authentication_exception__str__():
    exc = AuthenticationException("this is a test")
    assert str(exc) == "authentication exception: this is a test"
