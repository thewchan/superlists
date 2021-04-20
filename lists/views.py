"""Views to be served in the lists app."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    """Renders the hompage."""
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    """Renders the view list page."""
    list_ = List.objects.get(id=list_id)

    return render(request, "list.html", {"list": list_})


def new_list(request: HttpRequest) -> HttpResponse:
    """Renders the new list page."""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)

    return redirect(f"/lists/{list_.id}/")


def add_item(request: HttpRequest, list_id: str) -> HttpResponse:
    """Renders the add item page."""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)

    return redirect(f"/lists/{list_.id}/")
