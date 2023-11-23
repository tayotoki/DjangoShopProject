from django import template
from django.db.models.base import ModelBase

register = template.Library()


@register.filter
def get_html_id(model: ModelBase):
    return f"{model._meta.model_name}{model.pk}"


@register.filter("string_slice", safe=True)
def get_slice(string: str, args):
    try:
        bits = []
        for arg in args.split(":"):
            if not arg:
                bits.append(None)
            else:
                bits.append(int(arg))

        return string[slice(*bits)]

    except (ValueError, TypeError):
        return string
