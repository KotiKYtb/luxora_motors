"""Middleware de protection de l'application admin via Tailscale."""

from pathlib import Path

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


def is_tailscale_active() -> bool:
    """Lit l'etat Tailscale ecrit par le script hote (scripts/tailscale-watch.ps1)."""
    status_file = Path(getattr(settings, "TAILSCALE_STATUS_FILE", "/shared/.tailscale_active"))
    if not status_file.is_file():
        return False
    return status_file.read_text(encoding="utf-8-sig").strip().lower() in {
        "1", "true", "yes", "on", "connected"
    }


class TailscaleAdminMiddleware(MiddlewareMixin):
    """
    Autorise l'admin sur localhost uniquement si Tailscale est actif sur la machine hote.

    - Tailscale actif + http://127.0.0.1:8001 -> acces admin autorise.
    - Tailscale inactif -> redirection vers le site public (8000).
    """

    def process_request(self, request):
        if not getattr(settings, "TAILSCALE_ADMIN_REQUIRED", True):
            return None

        host = request.get_host().split(":")[0].lower()
        if host not in {"127.0.0.1", "localhost", "::1"}:
            return HttpResponseRedirect(settings.PUBLIC_SITE_URL)

        if is_tailscale_active():
            return None

        return HttpResponseRedirect(settings.PUBLIC_SITE_URL)
