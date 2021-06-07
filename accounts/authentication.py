"""Authentication backend for accoutns app."""
from typing import Union

from django.db import models

from accounts.models import Token, User


class PasswordlessAuthenticationBackend:
    """Backend for passwordless authentication"""

    def authenticate(self, uid: str) -> Union[None, models.Model]:
        """Authenticate user."""
        try:
            token = Token.objects.get(uid=uid)

            return User.objects.get(email=token.email)

        except User.DoesNotExist:
            return User.objects.create(email=token.email)

        except Token.DoesNotExist:
            return None

    def get_user(self, email: str) -> Union[None, models.Model]:
        """Retrieve user."""
        try:
            return User.objects.get(email=email)

        except User.DoesNotExist:
            return None
