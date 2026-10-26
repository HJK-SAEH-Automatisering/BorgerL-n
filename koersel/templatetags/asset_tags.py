import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def static_v(path):
    """Som {% static %}, men med filens ændringstidspunkt som ?v=.

    Versionen læses ved hver visning (én os.stat), så den også følger en ændring,
    mens serveren kører. Findes filen ikke, returneres adressen uden version.
    """
    url = static(path)
    fundet = finders.find(path)
    if not isinstance(fundet, str):
        return url
    try:
        version = os.stat(fundet).st_mtime_ns
    except OSError:
        return url
    return f"{url}?v={version}"
