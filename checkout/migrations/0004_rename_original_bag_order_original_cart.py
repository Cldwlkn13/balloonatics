# Generated by Django 3.2.3 on 2021-06-03 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20210603_1214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='original_bag',
            new_name='original_cart',
        ),
    ]