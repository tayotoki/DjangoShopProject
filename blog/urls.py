from django.urls import path

from .apps import BlogConfig
from .views import MainPageView, PostDetail, PostCreateView, PostUpdateView, SearchPageView

app_name = BlogConfig.name

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("post/<str:slug>-<uuid:uuid>", PostDetail.as_view(), name="post-detail"),
    path("post/create", PostCreateView.as_view(), name="post-create"),
    path("post/<str:slug>-<uuid:uuid>/update", PostUpdateView.as_view(), name="post-update"),
    path("search-results/", SearchPageView.as_view(), name="search-results"),
]
