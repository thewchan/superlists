"""Test suite for account app's views."""
from unittest.mock import call, MagicMock, patch
from django.db.models.manager import Manager

from django.test import TestCase

from accounts.models import Token


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    """Test suites for logging in."""

    def test_redirects_to_home_page(self, mock_auth: MagicMock) -> None:
        """Test for redirection to home page after loggin in."""
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")

    def test_calls_authenticate_with_uid_from_get_request(
        self, mock_auth: MagicMock
    ) -> None:
        """Test that login attempts triggers authentication backend."""
        self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(mock_auth.authenticate.call_args, call(uid="abcd123"))

    def test_calls_auth_login_with_user_if_there_is_one(
        self, mock_auth: MagicMock
    ) -> None:
        """Test that login from existing user works."""
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value),
        )

    def test_does_not_login_if_user_is_not_authenticated(
        self, mock_auth: MagicMock
    ) -> None:
        """Test rejection of user if login fails."""
        mock_auth.authenticate.return_value = None
        self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(mock_auth.login.called, False)


class SendLoginEmailViewTest(TestCase):
    """Test suite for testing emails."""

    def test_redirects_to_home_page(self) -> None:
        """Test after sending email user is redirected to home page."""
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "thewchan.misc@gmail.com"},
        )
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(
        self, mock_send_mail: MagicMock
    ) -> None:
        """Test successfully send email when user logs in."""
        self.client.post(
            "/accounts/send_login_email",
            data={"email": "thewchan.misc@gmail.com"},
        )

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(to_list, ["thewchan.misc@gmail.com"])

    def test_adds_success_message(self) -> None:
        """Test successful messaging."""
        response = self.client.post(
            "/accounts/send_login_email",
            data={"email": "edith@example.com"},
            follow=True,
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in.",
        )
        self.assertEqual(message.tags, "success")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(
        self, mock_send_mail: MagicMock
    ) -> None:
        """Test token works with sending login email."""
        self.client.post(
            "/accounts/send_login_email",
            data={"email": "thewchan.misc@gmail.com"},
        )
        token = Token.objects.first()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_creates_token_associated_with_email(self) -> None:
        """Test successful creation of token."""
        self.client.post(
            "/accounts/send_login_email",
            data={"email": "thewchan.misc@gmail.com"},
        )
        token = Token.objects.first()
        self.assertEqual(token.email, "thewchan.misc@gmail.com")
