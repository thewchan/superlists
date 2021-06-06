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
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(data=request.POST)

        if form.is_valid():
            Item.objects.create(text=request.POST["text"], list=list_)

            return redirect(list_)

    return render(request, "list.html", {"list": list_, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    """Renders the creation of a new list."""
    form = ItemForm(data=request.POST)

    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=list_)

        return redirect(list_)

    else:
        return render(request, "home.html", {"form": form})
