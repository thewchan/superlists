"""Test suite for authentication."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token


User = get_user_model()


class AuthenticateTest(TestCase):
    """Test suite for authentication."""

    def test_returns_None_if_no_such_token(self) -> None:
        """Test that None is returned if token does not exist."""
        result = PasswordlessAuthenticationBackend().authenticate(
            "no-such-token"
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self) -> None:
        """Test correct email is return for valid token."""
        email = "thewchan.misc@gmail.com"
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(
        self,
    ) -> None:
        """Test successful retrieval of email for existing token."""
        email = "thewchan.misc@gmail.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    """Test suite for retrieving user."""

    def test_gets_user_by_email(self) -> None:
        """Test emails are linked to correct user."""
        User.objects.create(email="mychan@vt.edu")
        desired_user = User.objects.create(email="thewchan.misc@gmail.com")
        found_user = PasswordlessAuthenticationBackend().get_user(
            "thewchan.misc@gmail.com"
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self) -> None:
        """Test non-existing user returns None."""
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(
                "thewchan.misc@gmail.com"
            )
        )
