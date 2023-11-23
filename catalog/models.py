import decimal

from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class BaseContent(models.Model):
    name = models.CharField(verbose_name="название", max_length=50)
    description = models.TextField(verbose_name="описание", null=True, blank=True)

    class Meta:
        abstract = True


class Category(BaseContent):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(BaseContent):
    preview = models.ImageField(verbose_name="превью", upload_to="images", null=True, blank=True)
    price = models.DecimalField(verbose_name="цена за покупку",
                                max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(decimal.Decimal("0.00"))])
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)

    category = models.ForeignKey(Category, verbose_name="категория", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Contact(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.title
