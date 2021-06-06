"""Test suite for models unit tests."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelsTest(TestCase):
    """Test suite for Item model."""

    def test_default_text(self) -> None:
        """Test default text correctly rendered."""
        item = Item()
        self.assertEqual(item.text, "")


class ListModelsTest(TestCase):
    """Test suite for List model."""

    def test_item_is_related_to_list(self) -> None:
        """Test item is in the right list."""
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self) -> None:
        """Test that empty list items is not saved to database."""
        list_ = List.objects.create()
        item = Item(list=list_, text="")

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self) -> None:
        """Test url are correctly generated."""
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f"/lists/{list_.id}/")

    def test_duplicate_items_are_invalid(self) -> None:
        """Test that duplicate items are marked as invalid."""
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="bla")

        with self.assertRaises(ValidationError):
            item = Item(list=list_, text="bla")
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        """Test duplicate items can be saved to separate lists."""
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        item = Item(list=list2, text="bla")
        item.full_clean()  # should not raise

    def test_list_ordering(self) -> None:
        """Test the ordering of the list."""
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="i1")
        item2 = Item.objects.create(list=list1, text="item 2")
        item3 = Item.objects.create(list=list1, text="3")
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])

    def test_string_representation(self) -> None:
        """Test the string representation of items."""
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")
