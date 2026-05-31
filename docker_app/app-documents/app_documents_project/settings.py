"""Settings Django de l'application documents (port 8002)."""

import os

from config.settings_base import *  # noqa: F403,F401

INSTALLED_APPS = ["django.contrib.admin", "documents"] + INSTALLED_APPS  # noqa: F405

ROOT_URLCONF = "app_documents_project.urls"
WSGI_APPLICATION = "app_documents_project.wsgi.application"
ASGI_APPLICATION = "app_documents_project.asgi.application"

LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/"

SESSION_COOKIE_NAME = "luxora_documents_sessionid"
CSRF_COOKIE_NAME = "luxora_documents_csrftoken"

TAILSCALE_ADMIN_REQUIRED = os.getenv("TAILSCALE_ADMIN_REQUIRED", "1") in {"1", "true", "True"}
PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL", "http://127.0.0.1:8000")
PUBLIC_SITE_PORT = os.getenv("PUBLIC_SITE_PORT", "8000")
PUBLIC_SITE_USE_REQUEST_HOST = os.getenv("PUBLIC_SITE_USE_REQUEST_HOST", "1") in {"1", "true", "True"}
TAILSCALE_STATUS_FILE = os.getenv("TAILSCALE_STATUS_FILE", "/shared/.tailscale_active")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "core.middleware.TailscaleAdminMiddleware",
    *MIDDLEWARE[1:],  # noqa: F405
]
