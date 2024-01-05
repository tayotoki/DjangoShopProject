from django.db.models import Q, Value, F, Prefetch
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product, Contact
from .forms import ProductCreateForm, FeedbackForm
from .generic import FormListView
from .mixins import AddVersionsFormsetMixin


class MainPage(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 8
    ordering = "-modified_at"

    def get_queryset(self):
        queryset = self.model.objects.order_by("-created_at").prefetch_related("versions")
        return queryset


class ShowProduct(DetailView):
    model = Product
    template_name = "catalog/product.html"
    context_object_name = "product"


class CreateProduct(AddVersionsFormsetMixin, CreateView):
    form_class = ProductCreateForm
    template_name = "catalog/create_product.html"


class UpdateProduct(AddVersionsFormsetMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "catalog/edit_product.html"


class Contacts(FormListView):
    model = Contact
    template_name = "catalog/contacts.html"
    form_class = FeedbackForm
    success_url = "."

    def form_valid(self, form):
        messages.success(self.request, _("Thanks for your feedback"))
        return super().form_valid(form)
