import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .models import Post
from .forms import CreateUpdatePostForm
from typing import Optional, Any


class PostCreateUpdateMixin:
    def __init_subclass__(cls, /, template_name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.template_name = template_name

    model = Post
    form_class = CreateUpdatePostForm


class PublishedPostsMixin:
    queryset = Post.posts.published().order_by("-created_at")


class PostBySlugAndUuidMixin(PublishedPostsMixin):
    kwargs: dict[str, Any]  # CBV instance attr

    def get_object_by_slug_and_uuid(self):
        uuid, slug = [self.kwargs.get(param) for param in ("uuid", "slug")]
        return self.queryset.filter(uuid_field=uuid, slug=slug)
