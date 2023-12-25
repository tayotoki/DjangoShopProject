from collections.abc import Sequence

from django.db import models
from django.db.models import F


class PostsManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)

    def not_published(self):
        return self.get_queryset().filter(is_published=False)

    def best_five_posts(self):
        return self.published().order_by("-views_count")[:5]

    def update_views(self, pk: int | Sequence[int]):
        if isinstance(pk, (str, bytes)):
            return

        if isinstance(pk, int):
            self.published().filter(pk=pk).update(views_count=F("views_count") + 1)
        elif isinstance(pk, Sequence):
            self.published().filter(pk__in=pk).update(views_count=F("views_count") + 1)
