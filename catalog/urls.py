from django.urls import path

from .views import index, contacts, product, create_product
from .apps import CatalogConfig

app_name = CatalogConfig.name


urlpatterns = [
    path("", index, name="index"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>", product, name="product"),
    path("product/new", create_product, name="create_product"),
]