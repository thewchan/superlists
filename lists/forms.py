"""Forms for to-do list app."""
from django import forms

from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    """Blueprint for forms."""

    class Meta:
        """Meta information for the item form."""

        model = Item
        fields = ("text",)
        widgets = {
            "text": forms.fields.TextInput(
                attrs={
                    "placeholder": "Enter a to-do item",
                    "class": "form-control input-lg",
                }
            ),
        }
        error_messages = {
            "text": {"required": EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        """Save item in form to list."""
        self.instance.list = for_list

        return super().save()
