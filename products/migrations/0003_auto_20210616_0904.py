# Generated by Django 3.2.3 on 2021-06-16 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_is_bundle_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='full_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_bundle_product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='message_editable',
        ),
    ]
