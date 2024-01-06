from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Post
from .mixins import PublishedPostsMixin, PostCreateUpdateMixin, PostBySlugAndUuidMixin
from .service.infrastructure.posts_service import PostsService


class SearchPageView(PublishedPostsMixin, ListView):
    model = Post
    template_name = "blog/search-result.html"
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get("search")

        if query:
            search_result = self.model.posts.get_search_results(search_term=query)
            result = search_result
        else:
            result = []

        return result


class MainPageView(PublishedPostsMixin, ListView):
    model = Post
    template_name = "blog/index.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list)
        context.update(
            {"best_five_posts": self.model.posts.best_five_posts()}
        )
        return context


class PostDetail(PostBySlugAndUuidMixin, DetailView):
    model = Post
    template_name = "blog/single-post.html"

    @PostsService.update_fields(fields=["views_count"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = self.get_object_by_slug_and_uuid()

        return super().get_object(queryset=queryset)


class PostCreateView(PostCreateUpdateMixin, CreateView, template_name="blog/create-post.html"):
    pass


class PostUpdateView(PostCreateUpdateMixin, UpdateView, template_name="blog/update-post.html"):
    pass
