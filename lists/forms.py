"""Forms for to-do list app."""
from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item


DUPLICATE_ITEM_ERROR = "You've already got this in your list"
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


class ExistingListItemForm(ItemForm):
    """A form for an already existing to-do list."""

    def __init__(self, for_list, *args, **kwargs):
        """Initialize form>"""
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        """Validate form's entries are unique."""
        try:
            self.instance.validate_unique()

        except ValidationError as error:
            error.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(error)
