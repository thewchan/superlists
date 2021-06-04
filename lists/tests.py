"""Unit test suites for to-do list."""
from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """Test suit for home page."""

    def test_root_url_resolves_to_home_page_view(self):
        """Test correct url resolution to home page."""
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """Test correct rendering of home page."""
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))
