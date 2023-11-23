from django.contrib import admin
from django.http import HttpRequest
# from django.utils import timezone
from datetime import date
import calendar
import re


class BaseMonthFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        return (
            ("1", "январь"),
            ("2", "февраль"),
            ("3", "март"),
            ("4", "апрель"),
            ("5", "май"),
            ("6", "июнь"),
            ("7", "июль"),
            ("8", "август"),
            ("9", "сентябрь"),
            ("10", "октябрь"),
            ("11", "ноябрь"),
            ("12", "декабрь"),
        )

    def has_output(self):
        return True


class MonthFilter(BaseMonthFilter):
    parameter_name = 'created_at__month'
    title = 'Фильтр по выбранному месяцу'
    field_name = "created_at"

    def queryset(self, request: HttpRequest, queryset):
        value = self.value()
        get_params = request.META.get("HTTP_REFERER")

        if value is not None:
            try:
                user_month = int(value.strip())
            except ValueError:
                return

            if user_month not in range(1, 13):
                return

            if "year" in get_params:
                date_pattern = re.compile(r'created_at__year=(\d{4})')
                data = re.findall(date_pattern, get_params)
                if data:
                    year = int(data[0])
            else:
                year = date.today().year

            end_day = calendar.monthrange(year, user_month)[1]
            start_day = 1
            last_date = date(year, user_month, end_day)
            start_date = last_date.replace(day=start_day)

            first_param, second_param = (
                self.field_name + "__gte",
                self.field_name + "__lte",
            )

            return queryset.filter(**{first_param: start_date,
                                      second_param: last_date})

        return queryset


class BaseYearFilter(admin.SimpleListFilter):
    def lookups(self, request, model_admin):
        years = {obj.created_at.year for obj in model_admin.model.objects.all()}

        return tuple(
            (str(year), str(year))
            for year in years
        )

    def has_output(self):
        return True


class YearFilter(BaseYearFilter):
    parameter_name = "created_at__year"
    title = "Фильтр по году"
    field_name = "created_at"

    def queryset(self, request, queryset):
        if (year := self.value()) is not None:
            return queryset.filter(
                created_at__gte=date(year=int(year), month=1, day=1),
                created_at__lt=date(year=int(year) + 1, month=1, day=1)
            )

        return queryset
