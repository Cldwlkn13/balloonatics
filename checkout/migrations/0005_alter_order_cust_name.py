# Generated by Django 3.2.3 on 2021-06-25 16:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20210625_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cust_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only characters are allowed.')]),
        ),
    ]
