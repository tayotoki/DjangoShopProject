from django.forms import ModelForm
from django.forms.widgets import Textarea, TextInput

from .models import Product


class ProductForm(ModelForm):
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