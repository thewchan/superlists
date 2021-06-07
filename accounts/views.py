"""The views of the accounts app."""
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from accounts.models import Token


def send_login_email(request: HttpRequest) -> HttpResponse:
    """Send login email for users trying to login."""
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid)
    )
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        "Your login link for Superlists",
        message_body,
        "noreply@superlists",
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect("/")


def login(request: HttpRequest) -> HttpResponse:
    """Return success login page."""
    user = auth.authenticate(uid=request.GET.get("token"))

    if user:
        auth.login(request, user)

    return redirect("/")
