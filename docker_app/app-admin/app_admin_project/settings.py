"""Settings Django de l'application d'administration."""

import os

from config.settings_base import *  # noqa: F403,F401

INSTALLED_APPS = ["django.contrib.admin"] + INSTALLED_APPS  # noqa: F405

ROOT_URLCONF = "app_admin_project.urls"
WSGI_APPLICATION = "app_admin_project.wsgi.application"
ASGI_APPLICATION = "app_admin_project.asgi.application"

LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/cms/"

# Evite les collisions de cookies entre app_user (8000) et app_admin (8001)
SESSION_COOKIE_NAME = "luxora_admin_sessionid"
CSRF_COOKIE_NAME = "luxora_admin_csrftoken"

# Acces admin localhost reserve si Tailscale actif (desactive avec TAILSCALE_ADMIN_REQUIRED=0)
TAILSCALE_ADMIN_REQUIRED = os.getenv("TAILSCALE_ADMIN_REQUIRED", "1") in {"1", "true", "True"}
PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL", "http://127.0.0.1:8000")
TAILSCALE_STATUS_FILE = os.getenv("TAILSCALE_STATUS_FILE", "/shared/.tailscale_active")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.TailscaleAdminMiddleware",
    *MIDDLEWARE[1:],  # noqa: F405
]
