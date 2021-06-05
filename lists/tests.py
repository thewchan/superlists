"""Test suite for list app."""
from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    """Test suite for to-do list homepage."""

    def test_uses_home_template(self) -> None:
        """Test for homepage rendering."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_returns_correct_html(self) -> None:
        """Test the home page links to correct html code."""
        response = self.client.get("/")
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    """Test suite for Django models."""

    def test_saving_and_retrieving_items(self) -> None:
        """Test database transactions."""
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
    """Test suit for the to-do list itself."""

    def test_uses_list_template(self):
        """Test the list template is used."""
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_items(self):
        """Test that all items in list is displayed."""
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")


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
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")
