from typing import Optional

from blog.models import Post


class PostsService:
    @classmethod
    def update_fields(cls, fields: Optional[list[str]]):
        def decorator(func: callable):
            def wrapper(view_obj_ref, *args, **kwargs):

                result = func(view_obj_ref, *args, **kwargs)
                fields_intersection = set(fields) & set(field.name for field in
                                                        view_obj_ref.model._meta.fields)

                for field in fields_intersection:
                    updater = getattr(cls, f"update_{field}", None)

                    if updater:
                        updater(view_obj_ref.object)

                return result
            return wrapper
        return decorator

    @classmethod
    def update_views_count(cls, obj_ref: Post):
        Post.posts.update_views(pk=obj_ref.pk)
