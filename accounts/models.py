"""Models for the accoutns app."""
import uuid

from django.contrib import auth
from django.db import models


auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    """The model for the user."""

    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    """The model for authentication tokens."""

    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)
