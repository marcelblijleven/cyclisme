from django.urls import path

from cyclisme.apps.authenticate.views import login_view, login_callback, login_redirect

urlpatterns = [
    path("login/", login_view, name="login"),
    path("login/redirect", login_redirect, name="login-redirect"),
    path("login/callback", login_callback, name="login-callback")
]
