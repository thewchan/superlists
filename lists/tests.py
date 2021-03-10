"""Unit tests for the lists app of superlist."""
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """Test for home page rendering."""

    def test_home_page_returns_currect_html(self) -> None:
        """Test if the home page response with the correct html."""
        response = self.client.get("")
        self.assertTemplateUsed(response, "home.html")
