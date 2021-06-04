"""Test suite for list app."""
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTest(TestCase):
    """Test suite for to-do list homepage."""

    def test_root_url_resolves_to_home_page_view(self):
        """Test for homepage rendering."""
        found = resolve("/")
        self.assertEqual(found.func, home_page)
