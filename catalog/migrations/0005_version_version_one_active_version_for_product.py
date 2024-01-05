# Generated by Django 4.2.7 on 2024-01-05 09:23

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='версия')),
                ('name', models.CharField(max_length=150, verbose_name='название')),
                ('is_active', models.BooleanField(default=False, verbose_name='активная')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='catalog.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
        migrations.AddConstraint(
            model_name='version',
            constraint=models.UniqueConstraint(condition=models.Q(('is_active', True)), fields=('product',), name='one_active_version_for_product'),
        ),
    ]
