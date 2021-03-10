"""Views to be served in the lists app."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_page(request: HttpRequest) -> HttpResponse:
    """Renders the hompage."""
    return render(request, "home.html")