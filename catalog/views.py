from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product, Contact
from .forms import ProductCreateForm, FeedbackForm
from .generic import FormListView


class MainPage(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-modified_at")


class ShowProduct(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])


class CreateProduct(CreateView):
    form_class = ProductCreateForm
    template_name = "create_product.html"


class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "edit_product.html"


class Contacts(FormListView):
    model = Contact
    template_name = "contacts.html"
    form_class = FeedbackForm
    success_url = "."

    def form_valid(self, form):
        messages.success(self.request, _("Thanks for your feedback"))
        return super().form_valid(form)
