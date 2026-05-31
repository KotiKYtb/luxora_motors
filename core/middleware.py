"""Middleware de protection des apps admin/documents via Tailscale."""

from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


def is_tailscale_active() -> bool:
    """Lit l'etat Tailscale ecrit par le script hote (tailscale-watch)."""
    status_file = Path(getattr(settings, "TAILSCALE_STATUS_FILE", "/shared/.tailscale_active"))
    if not status_file.is_file():
        return False
    return status_file.read_text(encoding="utf-8-sig").strip().lower() in {
        "1", "true", "yes", "on", "connected"
    }


def public_site_redirect_url(request) -> str:
    """
    URL de redirection vers le site public (8000).
    Reprend l'hote de la requete (IP serveur ou localhost) si possible.
    """
    configured = getattr(settings, "PUBLIC_SITE_URL", "http://127.0.0.1:8000")
    public_port = getattr(settings, "PUBLIC_SITE_PORT", "8000")

    if getattr(settings, "PUBLIC_SITE_USE_REQUEST_HOST", True):
        host = request.get_host().split(":")[0]
        parsed = urlparse(configured)
        scheme = parsed.scheme or ("https" if request.is_secure() else "http")
        return f"{scheme}://{host}:{public_port}/"

    return configured


class TailscaleAdminMiddleware(MiddlewareMixin):
    """
    Protege admin/documents : acces autorise uniquement si Tailscale est actif sur le serveur.

    - Site public (8000) : non concerne par ce middleware.
    - CMS (8001) et documents (8002) : accessibles via IP serveur ou localhost si Tailscale actif.
    - Tailscale inactif : redirection vers le site public sur le meme hote (port 8000).
    """

    def process_request(self, request):
        if not getattr(settings, "TAILSCALE_ADMIN_REQUIRED", True):
            return None

        if is_tailscale_active():
            return None

        return HttpResponseRedirect(public_site_redirect_url(request))
