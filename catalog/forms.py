from django import forms
from django.forms.widgets import Textarea, TextInput

from .models import Product


class ProductCreateForm(forms.ModelForm):
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


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
