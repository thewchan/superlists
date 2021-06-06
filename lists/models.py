"""Django models to to-do list app."""
from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    """Database object for the to-do list itself."""

    def get_absolute_url(self):
        """Return aboslute url of view."""
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    """Database object for to-do list items."""

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None)  # noqa: VNE003

    class Meta:
        """Meta information for the item model."""

        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self):
        """Overloads string method."""
        return self.text
