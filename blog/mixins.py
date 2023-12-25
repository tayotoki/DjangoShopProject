from .models import Post
from typing import Optional


class PublishedPostsMixin:
    queryset = Post.posts.published()