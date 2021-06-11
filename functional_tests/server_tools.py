"""Helper deployment server functions."""
from typing import Dict

from fabric.api import run
from fabric.context_managers import shell_env, settings


def _get_manage_dot_py(host: str) -> str:
    """Return the path of manage.py."""
    return f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/manage.py"


def reset_database(host: str) -> None:
    """Reset the current django database."""
    manage_dot_py = _get_manage_dot_py(host)

    with settings(host_string=f"pi@{host}"):
        run(f"{manage_dot_py} flush --noinput")


def _get_server_env_vars(host: str) -> Dict:
    """Retrieve envrionmental variables from the server."""
    env_lists = run(f"cat ~/sites{host}/.env").splitlines()

    return dict(l.split("=") for l in env_lists if l)


def create_session_on_server(host: str, email: str) -> str:
    """Create django session on server and return the session key."""
    manage_dot_py = _get_manage_dot_py(host)

    with settings(host_string=f"pi@{host}"):
        env_vars = _get_server_env_vars(host)

        with shell_env(**env_vars):
            session_key = run(f"{manage_dot_py} create_session {email}")

            return session_key.strip()
