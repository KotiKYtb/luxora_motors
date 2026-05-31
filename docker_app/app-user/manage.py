#!/usr/bin/env python
"""Django command-line utility for app-user."""
import os
import sys
from pathlib import Path


def main():
    shared_root_env = os.getenv("SHARED_PROJECT_ROOT")
    if shared_root_env:
        shared_root = Path(shared_root_env)
    else:
        shared_root = Path(__file__).resolve().parent
    if str(shared_root) not in sys.path:
        sys.path.insert(0, str(shared_root))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_user_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
