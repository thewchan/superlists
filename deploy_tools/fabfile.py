import random

from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed


REPO_URL = "https://github.com/thewchan/superlists.git"


def deploy() -> None:
    """Deploy site via fabric3."""
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = f"{site_folder}/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder: str) -> None:
    """Create directory structure of the website."""
    for subfolder in ("database", "static", "virtualenv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source(source_folder: str) -> None:
    """Get the latest source code of the website."""
    if exists(f"{source_folder}/.git"):
        run(f"cd {source_folder} && git fetch")

    else:
        run(f"git clone {REPO_URL} {source_folder}")

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_settings(source_folder: str,site_name: str) -> None:
    """Update the settings.py django config file for the website."""
    settings_path = f"{source_folder}/superlists/settings.py"
    sed(settings_path, r"DEBUG = True", r"DEBUG = False")
    sed(
        settings_path,
        r"ALLOWED_HOSTS =.+$",
        fr'ALLOWED_HOSTS = ["{site_name}"]',
    )
    secret_key_file = f"{source_folder}/superlists/secret_key.py"

    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(_-=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')

    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder: str) -> None:
    """Update the virtual environment and dependencies for the website."""
    virtualenv_folder = f"{source_folder}/../virtualenv"

    if not exists(f"{virtualenv_folder}/bin/pip"):
        run(f"python3 -m venv {virtualenv_folder}")

    run(f"{virtualenv_folder}/bin/python3 -m pip install -r "
        + f"{source_folder}/requirements.txt")


def _update_static_files(source_folder: str) ->  None:
    """Update the static files for the website."""
    run(
        f"cd {source_folder} "
        + "&& ../virtualenv/bin/python3 manage.py collectstatic --noinput"
    )


def _update_database(source_folder: str) -> None:
    """Update/migrate the django database."""
    run(f"cd {source_folder} "
        + "&& ../virtualenv/bin/python3 manage.py migrate --noinput")
