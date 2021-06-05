"""Test suite for list app."""
from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    """Test suite for to-do list homepage."""

    def test_uses_home_template(self) -> None:
        """Test for homepage rendering."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self) -> None:  # noqa: N802
        """Test that a POST request can be saved."""
        self.client.post("/", data={"item_text": "A new list item"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self) -> None:  # noqa: N802
        """Test redirection after a POST request."""
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_home_page_returns_correct_html(self) -> None:
        """Test the home page links to correct html code."""
        response = self.client.get("/")
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))
        self.assertTemplateUsed(response, "home.html")

    def test_only_saves_items_when_necessary(self) -> None:
        """Test to-do list items are saved appropriately."""
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self) -> None:
        """Test that multiple list items are rendered."""
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/")

        self.assertIn("itemey 1", response.content.decode())
        self.assertIn("itemey 2", response.content.decode())


class ItemModelTest(TestCase):
    """Test suite for Django models"""

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
