from django.urls import path

from cyclisme.apps.base.views.home import home

urlpatterns = [
    path("", home, name="home")
]
