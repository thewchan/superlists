"""Test suite for account app models."""
from django.contrib import auth
from django.test import TestCase

from accounts.models import Token


User = auth.get_user_model()


class UserModelTest(TestCase):
    """Test suite for the user model."""

    def test_user_is_valid_with_email_only(self) -> None:
        """Test that only email is needed for a user record."""
        user = User(email="a@b.com")
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self) -> None:
        """Test that email field is the primary key for user db entry."""
        user = User(email="a@b.com")
        self.assertEqual(user.pk, "a@b.com")

    def test_no_problem_with_auth_login(self) -> None:
        """Test successful auth login."""
        user = User.objects.create(email="thewchan.misc@gmail.com")
        user.backend = ""
        request = self.client.request().wsgi_request
        auth.login(request, user)  # should not raise


class TokenModelTest(TestCase):
    """Test suite for authentication tokens."""

    def test_link_user_with_auto_generated_uid(self) -> None:
        """Test users are linked with the correct uid."""
        token1 = Token.objects.create(email="a@b.com")
        token2 = Token.objects.create(email="a@b.com")
        self.assertNotEqual(token1.uid, token2.uid)
