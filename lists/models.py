"""Django models to to-do list app."""
from django.db import models


class List(models.Model):
    """Database object for the to-do list itself."""


class Item(models.Model):
    """Database object for to-do list items."""

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None)  # noqa: VNE003
