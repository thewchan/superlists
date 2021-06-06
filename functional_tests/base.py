"""Functional tests helper functions."""
import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    """Helper functions for tests."""

    def setUp(self) -> None:
        """Set up browser."""
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server

    def tearDown(self) -> None:
        """Quit browser."""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text) -> None:
        """Test that a new row is added to to-do list, helper method."""
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])

                return

            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error

                time.sleep(0.5)
