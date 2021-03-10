"""Unit tests for the lists app of superlist."""
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """Test for home page rendering."""

    def test_root_url(self) -> None:
        """Test if '/' returns the homepage."""
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_currect_html(self) -> None:
        """Test if the home page response with the correct html."""
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8")

        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))
