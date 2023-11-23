from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import IntegrityError, ProgrammingError

from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        fixture_path: Path = settings.BASE_DIR / "catalog" / "fixtures"

        Category.objects.all().delete()
        Product.objects.all().delete()

        try:
            for fixture in list(fixture_path.iterdir())[::-1]:
                call_command("loaddata", fixture)
        except IntegrityError as e:
            self.stdout.write(f'Invalid fixtures: {e}', self.style.NOTICE)
        except ProgrammingError:
            pass
        else:
            self.stdout.write(
                'Command have been completed successfully', self.style.SUCCESS
            )
