"""Functional tests helper functions."""
import os
import time
from typing import Callable

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

from .server_tools import reset_database


MAX_WAIT = 10


def wait(fn: Callable) -> Callable:
    """Transform function to a wait function."""
    def modified_fn(*args, **kwargs) -> Callable:
        """Return modified function given outer function."""
        start_time = time.time()

        while True:
            try:
                return fn(*args, **kwargs)

            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error

                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    """Helper functions for tests."""

    def setUp(self) -> None:
        """Set up browser."""
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get("STAGING_SERVER")
        if self.staging_server:
            self.live_server_url = "http://" + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self) -> None:
        """Quit browser."""
        self.browser.quit()

    @wait
    def wait_for_row_in_list_table(self, row_text) -> None:
        """Test that a new row is added to to-do list, helper method."""
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn: Callable) -> None:
        """Wait for generic response."""
        return fn()

    def get_item_input_box(self) -> WebElement:
        """Return input box of list item."""
        return self.browser.find_element_by_id("id_text")

    @wait
    def wait_to_be_logged_in(self, email: str) -> None:
        """Test that user's email is in navbar."""
        self.browser.find_element_by_link_text("Log out")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email: str) -> None:
        """Test once log out user email is not in nav bar."""
        self.browser.find_element_by_name("email")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)
