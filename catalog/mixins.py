from django.forms import inlineformset_factory

from .forms import VersionInlineForm, VersionFormset
from .models import Product, Version


class AddVersionsFormsetMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        version_formset = inlineformset_factory(
            Product,
            Version,
            form=VersionInlineForm,
            extra=1,
            formset=VersionFormset
        )
        if self.request.method == "POST":
            context["formset"] = version_formset(self.request.POST, instance=self.object)
        else:
            context["formset"] = version_formset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]

        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        return super().form_invalid(form)
