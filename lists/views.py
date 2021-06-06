"""Django views for to-do list app."""
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    """Renders home page."""
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    """Renders to-do list."""
    list_ = List.objects.get(id=list_id)

    return render(request, "list.html", {"list": list_})


def new_list(request: HttpRequest) -> HttpResponse:
    """Renders the creation of a new list."""
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)

    try:
        item.full_clean()
        item.save()

    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})

    return redirect(f"/lists/{list_.id}/")


def add_item(request: HttpRequest, list_id: str) -> HttpResponse:
    """Renders the adding of items to to-do list."""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)

    return redirect(f"/lists/{list_.id}/")
