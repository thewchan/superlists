"""Fabric deployment configuration and script."""
import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/thewchan/superlists.git"


def deploy() -> None:
    """Deploy site to server."""
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source() -> None:
    """Fetch the latest source code."""
    if exists(".git"):
        run("git fetch")

    else:
        run(f"git clone {REPO_URL} .")

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _update_virtualenv() -> None:
    """Updates the virtual environment at the server."""
    if not exists("virtualenv/bin/pip"):
        run("python3.7 -m venv virtualenv")

    run("./virtualenv/bin/pip install -r requirements.txt")


def _create_or_update_dotenv() -> None:
    """Create or update environment file as needed."""
    append(".env", "DJANGO_DEBUG_FALSE=y")
    append(".env", f"SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(
            random.SystemRandom().choices(
                "abcdefghijklmnopqrstuvwxyz0123456789", k=50
            )
        )
        append(".env", f"DJANGO_SECRET_KEY={new_secret}")


def _update_static_files() -> None:
    """Update static files as needed."""
    run("./virtualenv/bin/python manage.py collectstatic --noinput")


def _update_database() -> None:
    """Migrate database as necessary."""
    run("./virtualenv/bin/python manage.py migrate --noinput")
