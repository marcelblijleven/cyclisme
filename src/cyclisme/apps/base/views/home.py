from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect


def home(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "home.html", context={})
