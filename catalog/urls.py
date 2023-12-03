from django.urls import path

from .views import MainPage, ShowProduct, CreateProduct, UpdateProduct, Contacts
from .apps import CatalogConfig

app_name = CatalogConfig.name


urlpatterns = [
    path("", MainPage.as_view(), name="index"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("product/<int:pk>", ShowProduct.as_view(), name="product"),
    path("product/new", CreateProduct.as_view(), name="create_product"),
    path("product/edit/<int:pk>", UpdateProduct.as_view(), name="edit_product"),
]