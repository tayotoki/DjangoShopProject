import functools
import re
from collections.abc import Callable
from typing import Optional, Any

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from .models import Product, Version


# TODO: вынести декоратор и общие валидаторы в отдельный модуль или пакет.
def common_text_validation(method: Callable[..., Any]):
    """Decorator for common text fields validations."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if (name := method.__name__).startswith("clean_"):

            field_name = name.split("_", 1)[-1]  # clean_{field} | clean_{some_field} -> field | some_field

            string = self.cleaned_data.get(field_name)
            self._validate_text(string=string)

            result = method(self, *args, **kwargs)

            return result.strip() if result else string.strip()
        raise ValueError("Invalid method %s for decoration in %s" % (name, self.__class__))
    return wrapper


class ProductCreateForm(forms.ModelForm):
    prohibited_names = {
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    }

    def _validate_text(self, string: Optional[str] = None):

        if any(
            {re.match(f"(?i).*(?P<name>{prohibited_name}).*", string)
             for prohibited_name in self.prohibited_names}
        ):
            raise ValidationError(
                _("This field contains prohibited words!")
            )

    @common_text_validation
    def clean_name(self):
        pass

    @common_text_validation
    def clean_description(self):
        pass

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "preview",
            "price",
            "category",
            "preview",
        ]

        widgets = {
            "description": Textarea(
                attrs={
                    "class": "form-control text-bg-light text row p-2 col-sm-3 m-xl-auto",
                    "style": "height: 200px",
                }
            ),
            "name": TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }


class VersionFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return

        counter = 0

        for form in self.forms:
            if form.cleaned_data.get("is_active"):
                counter += 1
            if counter > 1:
                raise forms.ValidationError("У продукта может быть только одна активная версия")


class VersionInlineForm(forms.ModelForm):
    class Meta:
        model = Version
        exclude = ("product", )

        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
