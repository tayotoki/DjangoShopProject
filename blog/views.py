from django.shortcuts import render
from django.views.generic import ListView

from .models import Post


# Create your views here.
class MainPageView(ListView):
    model = Post
    template_name = "blog/index.html"

    def get_queryset(self):
        return self.model.posts.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        best_five_posts = self.get_queryset().order_by("-views_count")[:5]
        context = super().get_context_data(object_list=object_list)
        context.update(
            {"best_five_posts": best_five_posts}
        )
        return context


