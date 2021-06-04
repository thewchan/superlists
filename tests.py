"""Test suite for list app."""
from django.test import TestCase


class SmokeTest(TestCase):
    """Test for tests."""

    def test_bad_maths(self) -> None:
        """Test failings."""
        self.assertEqual(1 + 1, 3)
