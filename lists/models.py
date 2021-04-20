"""Models in the list app."""
from django.db import models


class List(models.Model):
    """Generic list object for database ORM."""


class Item(models.Model):
    """Generic object for database ORM."""

    text: models.TextField = models.TextField(default="")
    list: models.ForeignKey = models.ForeignKey(List,
                                                on_delete=models.CASCADE,
                                                default=None)
