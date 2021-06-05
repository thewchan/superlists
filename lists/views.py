"""Django views for to-do list app."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item


def home_page(request: HttpRequest) -> HttpResponse:
    """Renders home page."""
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")

    items = Item.objects.all()

    return render(request, "home.html", {"items": items})
