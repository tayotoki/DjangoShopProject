from django import forms

from .models import Post
from .russian_slugify import alphabet, slugify, django_slugify


class CreateUpdatePostForm(forms.ModelForm):
    def save(self, commit=True):
        if not self.instance.slug:
            if set(self.instance.title) & alphabet.keys():
                self.instance.slug = slugify(self.instance.title)
            else:
                self.instance.slug = django_slugify(self.instance.title)

        return super().save(commit=commit)

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "preview",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите заголовок",
                    "id": "post-title"
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Напишите текст поста",
                    "id": "post-content",
                    "cols": "30",
                    "rows": "10"
                }
            )
        }

