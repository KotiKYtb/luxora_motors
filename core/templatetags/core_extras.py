"""Filtres template personnalisés (format nombre avec espaces pour milliers)."""
from django import template

register = template.Library()


@register.filter
def intspace(value):
    """Formate un nombre avec des espaces comme séparateurs de milliers (ex: 363 490)."""
    if value is None:
        return ""
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        return value
    s = str(n)
    if n < 0:
        s = s[1:]
        sign = "-"
    else:
        sign = ""
    # Groupes de 3 chiffres depuis la fin
    parts = []
    while len(s) > 3:
        parts.append(s[-3:])
        s = s[:-3]
    if s:
        parts.append(s)
    return sign + " ".join(reversed(parts))
