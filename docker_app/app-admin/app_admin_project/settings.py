"""Settings Django de l'application d'administration."""

import os

from config.settings_base import *  # noqa: F403,F401

INSTALLED_APPS = ["django.contrib.admin"] + INSTALLED_APPS  # noqa: F405

ROOT_URLCONF = "app_admin_project.urls"
WSGI_APPLICATION = "app_admin_project.wsgi.application"
ASGI_APPLICATION = "app_admin_project.asgi.application"

LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/cms/"

SESSION_COOKIE_NAME = "luxora_admin_sessionid"
CSRF_COOKIE_NAME = "luxora_admin_csrftoken"

TAILSCALE_ADMIN_REQUIRED = os.getenv("TAILSCALE_ADMIN_REQUIRED", "1") in {"1", "true", "True"}
TAILSCALE_ALLOW_LOCALHOST = os.getenv("TAILSCALE_ALLOW_LOCALHOST", "0") in {"1", "true", "True"}
TRUST_X_FORWARDED_FOR = os.getenv("TRUST_X_FORWARDED_FOR", "0") in {"1", "true", "True"}
TAILSCALE_ALLOWED_CLIENT_IPS = [
    ip.strip()
    for ip in os.getenv("TAILSCALE_ALLOWED_CLIENT_IPS", "").split(",")
    if ip.strip()
]
TAILSCALE_CLIENTS_FILE = os.getenv(
    "TAILSCALE_CLIENTS_FILE", "/shared/config/allowed_tailscale_ips.txt"
)
PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL", "http://127.0.0.1:8000")
PUBLIC_SITE_PORT = os.getenv("PUBLIC_SITE_PORT", "8000")
PUBLIC_SITE_USE_REQUEST_HOST = os.getenv("PUBLIC_SITE_USE_REQUEST_HOST", "1") in {"1", "true", "True"}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.TailscaleAdminMiddleware",
    *MIDDLEWARE[1:],  # noqa: F405
]
