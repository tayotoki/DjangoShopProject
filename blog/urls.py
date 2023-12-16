from django.urls import path

from .apps import BlogConfig
from .views import MainPageView

app_name = BlogConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
]
