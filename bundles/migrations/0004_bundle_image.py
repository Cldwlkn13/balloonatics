# Generated by Django 3.2.3 on 2021-06-10 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundles', '0003_bundleitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundle',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
