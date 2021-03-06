# Generated by Django 3.2.3 on 2021-06-22 08:47

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_id', models.CharField(editable=False, max_length=254)),
                ('name', models.CharField(max_length=254)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('custom', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BundleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'BundleCategories',
            },
        ),
        migrations.CreateModel(
            name='BundleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_qty', models.PositiveIntegerField(default=0)),
                ('item_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('bundle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bundle_items', to='bundles.bundle')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='bundle',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bundles.bundlecategory'),
        ),
        migrations.AddField(
            model_name='bundle',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
