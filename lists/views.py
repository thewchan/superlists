"""Django views for to-do list app."""
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    """Renders home page."""
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: str) -> HttpResponse:
    """Renders to-do list."""
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == "POST":
        try:
            item = Item(text=request.POST["text"], list=list_)
            item.full_clean()
            item.save()

            return redirect(list_)

        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, "list.html", {"list": list_, "error": error})


def new_list(request: HttpRequest) -> HttpResponse:
    """Renders the creation of a new list."""
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["text"], list=list_)

    try:
        item.full_clean()
        item.save()

    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})

    return redirect(list_)
