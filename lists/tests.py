"""Unit tests for the lists app of superlist."""
from django.test import TestCase


class SmokeTest(TestCase):
    """Sanity check test."""

    def test_bad_math(self):
        """Test if tests would be ran."""
        self.assertEqual(1 + 1, 3)
