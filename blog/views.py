from django.db.models import F
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from uuid import UUID

from .models import Post
from .mixins import PublishedPostsMixin
from .forms import CreateUpdatePostForm


# Create your views here.
class MainPageView(PublishedPostsMixin, ListView):
    model = Post
    template_name = "blog/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list)
        context.update(
            {"best_five_posts": self.model.posts.best_five_posts()}
        )
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "blog/single-post.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.model.posts.update_views(pk=self.object.pk)

        return response

    def get_object(self, queryset=None):
        uuid = self.kwargs.get("uuid")
        slug = self.kwargs.get("slug")

        queryset = self.get_queryset().filter(uuid_field=uuid, slug=slug)

        return super().get_object(queryset=queryset)


class PostCreateUpdateBase:
    model = Post
    form_class = CreateUpdatePostForm


class PostCreateView(PostCreateUpdateBase, CreateView):
    template_name = "blog/create-post.html"


class PostUpdateView(PostCreateUpdateBase, UpdateView):
    template_name = "blog/create-post.html"