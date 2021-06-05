"""Test suite for list app."""
from django.test import TestCase


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
