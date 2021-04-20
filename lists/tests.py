"""Unit tests for the lists app of superlist."""
from django.test import TestCase

from lists.models import Item, List


class HomePageTest(TestCase):
    """Test for home page rendering."""

    def test_uses_home_template(self) -> None:
        """Test if the home page renders from template."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListAndItemModelsTest(TestCase):
    """Test for ORM manipulation."""

    def test_saving_and_retrieving_items(self) -> None:
        """Test ability to save and retrieve item from database."""
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """Test for new URL rendering."""

    def test_uses_list_template(self) -> None:
        """Test that list is using a different URL."""
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_all_items(self) -> None:
        """Test the to-do list would display all items in database."""
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=other_list)
        Item.objects.create(text="itemey 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

    def test_passes_correct_list_to_template(self):
        """Test the correct list is passed to the list.html template."""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    """Test for making a new todo list."""

    def test_can_save_a_POST_request_to_an_existing_list(self) -> None:
        """Test if the home page can save the payload of a POST."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f"/lists/{correct_list.id}/add_item",
                         data={"item_text":
                               "A new item for an existing list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self) -> None:
        """Test if a POST request redirects back to home page."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f"/lists/{correct_list.id}/add_item",
                                    data={"item_text":
                                          "A new item for an existing list"})
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
