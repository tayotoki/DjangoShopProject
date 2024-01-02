from django.db.models.signals import post_save
from django.dispatch import receiver

from email_service.send import Message


@receiver(post_save, sender="blog.Post")
def mail_callback(sender, *args, **kwargs):
    post = kwargs.get("instance")

    Message.send_post_is_reached_views(post=post)
