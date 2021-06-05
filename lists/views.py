"""Django views for to-do list app."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    """Renders home page."""
    return render(request, "home.html")
