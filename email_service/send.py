from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.conf import settings

from blog.models import Post


class Message(EmailMessage):
    VIEWS_COUNT_TRIGGER = 100
    receivers_mails = settings.RECEIVERS_EMAILS

    @classmethod
    def send_post_is_reached_views(cls, post: Post):
        if post and post.views_count == cls.VIEWS_COUNT_TRIGGER:
            if settings.DEBUG:
                domain = "http://localhost:8000"
            else:
                current_site = Site.objects.get_current()
                domain = current_site.domain

            instance = cls(
                subject="Достигнуто %d просмотров у поста %s" % (post.views_count, post.title),
                to=cls.receivers_mails,
                body="У поста %s (%s) уже %d просмотров, поздравляем!" % (
                    post.title,
                    domain + post.get_absolute_url(),
                    post.views_count
                )
            )

            instance.send()
