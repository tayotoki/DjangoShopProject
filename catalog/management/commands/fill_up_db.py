import subprocess

from django.conf import settings
from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        subprocess.call(["sh", settings.BASE_DIR / "catalog" / "fixtures" / "load_all.sh"])
