from collections.abc import Callable

from .models import Post
from typing import Optional


class PublishedPostsMixin:
    queryset = Post.posts.published()


def update_post_views(method: Callable):
    def wrapper(obj_ref, request, *args, **kwargs):
        response = method(obj_ref, request, *args, **kwargs)
        obj_ref.model.posts.update_views(pk=obj_ref.object.pk)
        return response
    return wrapper
