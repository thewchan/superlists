"""Unit tests for the lists app of superlist."""
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """Test for home page rendering."""

    def test_root_url(self) -> None:
        """Test if '/' returns the homepage."""
        found = resolve("/")
        self.assertEqual(found.func, home_page)
