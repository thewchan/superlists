"""Unit tests for the lists app of superlist."""
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """Test for home page rendering."""

    def test_uses_home_template(self) -> None:
        """Test if the home page renders from template."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self) -> None:
        """Test if the home page can save the payload of a POST."""
        response = self.client.post("", data={"item_text": "A new list item"})
        self.assertIn("A new list item", response.content.decode())
        self.assertTemplateUsed(response,  "home.html")
