"""Settings Django de l'application publique."""

from config.settings_base import *  # noqa: F403,F401

ROOT_URLCONF = "app_user_project.urls"
WSGI_APPLICATION = "app_user_project.wsgi.application"
ASGI_APPLICATION = "app_user_project.asgi.application"

LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/"

# Evite les collisions de cookies entre app_user (8000) et app_admin (8001)
SESSION_COOKIE_NAME = "luxora_user_sessionid"
CSRF_COOKIE_NAME = "luxora_user_csrftoken"
