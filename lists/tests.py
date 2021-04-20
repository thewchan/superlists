"""Unit tests for the lists app of superlist."""
from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):
    """Test for home page rendering."""

    def test_uses_home_template(self) -> None:
        """Test if the home page renders from template."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    """Test for ORM manipulation."""

    def test_saving_and_retrieving_items(self) -> None:
        """Test ability to save and retrieve item from database."""
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")


class ListViewTest(TestCase):
    """Test for new URL rendering."""

    def test_uses_list_template(self) -> None:
        """Test that list is using a different URL."""
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self) -> None:
        """Test the to-do list would display all items in database."""
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")


class NewListTest(TestCase):
    """Test for making a new todo list."""

    def test_can_save_a_POST_request(self) -> None:
        """Test if the home page can save the payload of a POST."""
        self.client.post("/lists/new", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self) -> None:
        """Test if a POST request redirects back to home page."""
        response = self.client.post("/lists/new",
                                    data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")
