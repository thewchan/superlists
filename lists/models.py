"""Models in the list app."""
from django.db import models


class Item(models.Model):
    """Generic object for database ORM."""
    text = models.TextField(default="")
