# Generated by Django 3.2.3 on 2021-06-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_alter_product_bundle_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_bundle',
            field=models.BooleanField(default=False),
        ),
    ]
