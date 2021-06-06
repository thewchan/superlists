"""Test suite for views unit tests."""
from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    """Test suite for to-do list homepage."""

    def test_uses_home_template(self) -> None:
        """Test for homepage rendering."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    """Test suit for the to-do list itself."""

    def test_uses_list_template(self) -> None:
        """Test the list template is used."""
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self) -> None:
        """Test that all items in list is displayed for a list_."""
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_template(self) -> None:
        """Test list is passed to correct template for rendering."""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)


class NewListTest(TestCase):
    """Test suite for initializing new to-do lists."""

    def test_can_save_a_POST_request(self) -> None:  # noqa: N802
        """Test a POST request is correctly saved."""
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self) -> None:  # noqa: N802
        """Test correct redirection after a POST request."""
        response = self.client.post(
            "/lists/new", data={"item_text": "A new list item"}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")


class NewItemTest(TestCase):
    """Test suite for crating new list items."""

    def test_can_save_a_POST_request_to_an_existing_list(self) -> None:
        """Test a POST request can be made to existing lists."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """Test correct redirectional after adding items to list."""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")
