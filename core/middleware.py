"""Middleware : acces CMS/documents reserve aux IP Tailscale autorisees."""

import ipaddress
import logging
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


def _parse_ip(addr: str):
    try:
        return ipaddress.ip_address(addr.strip())
    except ValueError:
        return None


def get_client_ip(request):
    if getattr(settings, "TRUST_X_FORWARDED_FOR", False):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return _parse_ip(forwarded.split(",")[0])
    return _parse_ip(request.META.get("REMOTE_ADDR", ""))


def _load_allowed_client_ips() -> set[str]:
    ips = set(getattr(settings, "TAILSCALE_ALLOWED_CLIENT_IPS", []))

    clients_file = getattr(settings, "TAILSCALE_CLIENTS_FILE", "")
    if clients_file:
        path = Path(clients_file)
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                ips.add(line.split("#", 1)[0].strip())

    return ips


def client_is_allowed(request) -> bool:
    if getattr(settings, "TAILSCALE_ALLOW_LOCALHOST", False):
        host = request.get_host().split(":")[0].lower()
        if host in {"127.0.0.1", "localhost", "::1"}:
            return True

    client_ip = get_client_ip(request)
    if not client_ip:
        return False

    allowed = _load_allowed_client_ips()
    if not allowed:
        logger.warning("Liste blanche Tailscale vide — acces CMS/documents refuse.")
        return False

    return str(client_ip) in allowed


def public_site_redirect_url(request) -> str:
    configured = getattr(settings, "PUBLIC_SITE_URL", "http://127.0.0.1:8000")
    public_port = getattr(settings, "PUBLIC_SITE_PORT", "8000")

    if getattr(settings, "PUBLIC_SITE_USE_REQUEST_HOST", True):
        host = request.get_host().split(":")[0]
        parsed = urlparse(configured)
        scheme = parsed.scheme or ("https" if request.is_secure() else "http")
        return f"{scheme}://{host}:{public_port}/"

    return configured


class TailscaleAdminMiddleware(MiddlewareMixin):
    """Protege CMS (8001) et documents (8002) via liste blanche IP Tailscale."""

    def process_request(self, request):
        if not getattr(settings, "TAILSCALE_ADMIN_REQUIRED", True):
            return None

        if client_is_allowed(request):
            return None

        client_ip = get_client_ip(request)
        logger.info(
            "Acces CMS/documents refuse — IP cliente=%s, autorisees=%s",
            client_ip,
            sorted(_load_allowed_client_ips()),
        )
        return HttpResponseRedirect(public_site_redirect_url(request))
