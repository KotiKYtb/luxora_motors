"""Context processors partages aux applications Luxora."""


def luxora_service_urls(request):
    """URLs des 3 apps basees sur l'hote de la requete (localhost ou IP serveur)."""
    host = request.get_host().split(":")[0]
    scheme = "https" if request.is_secure() else "http"
    return {
        "LUXORA_PUBLIC_URL": f"{scheme}://{host}:8000",
        "LUXORA_CMS_URL": f"{scheme}://{host}:8001",
        "LUXORA_DOCUMENTS_URL": f"{scheme}://{host}:8002",
    }
