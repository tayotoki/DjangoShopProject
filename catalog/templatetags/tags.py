from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def mediapath(format_string) -> str:
    return f"{settings.MEDIA_URL}{format_string}"
