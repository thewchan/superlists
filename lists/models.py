"""Django models to to-do list app."""
from django.db import models


class Item(models.Model):
    """Database object for to-do list items."""

    text = models.TextField(default="")
