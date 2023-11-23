from django.contrib import admin
from .models import Product, Category, Contact
from django.db.models import Q

from . import filters

admin.site.register(Contact)


@admin.display(description="краткое описание")
def short_description(obj):
    return f"{obj.description[:35]}..."


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "modified_at")

    # TODO сделать фильтр по ценовым диапазонам поля price.
    list_filter = [
        "category",
        "created_at",
        filters.YearFilter,
        filters.MonthFilter
    ]
    list_display = [
        "id",
        "name",
        short_description,
        "price",
        "category",
    ]
    autocomplete_fields = ("category",)
    list_display_links = list_display
    search_fields = ("name", "description")
    search_help_text = "Введите название товара, категорию или часть описания"

    def get_search_results(self, request, queryset, search_term):
        queryset, distinct = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            queryset &= self.model.objects.filter(
                Q(name__iregex=search_term) | Q(description__icontains=search_term)
            )

        return queryset, distinct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", short_description)
    search_fields = ("name",)
