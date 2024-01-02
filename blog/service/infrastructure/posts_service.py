from typing import Optional

from blog.models import Post


class PostsService:
    @classmethod
    def update_fields(cls, fields: Optional[list[str]]):
        def decorator(func: callable):
            def wrapper(view_obj_ref, *args, **kwargs):

                response = func(view_obj_ref, *args, **kwargs)
                fields_intersection = set(fields) & set(field.name for field in
                                                        view_obj_ref.model._meta.fields)  # noqa

                for field in fields_intersection:
                    # Search update method for this field.
                    updater = getattr(cls, f"update_{field}", None)

                    if updater:
                        updater(view_obj_ref.object)

                return response
            return wrapper
        return decorator

    @classmethod
    def update_views_count(cls, post: Post):
        Post.posts.update_views(pk=post.pk)
