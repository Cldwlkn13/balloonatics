# Generated by Django 3.2.3 on 2021-06-16 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cust_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cust_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('street_address_1', models.CharField(blank=True, max_length=100, null=True)),
                ('street_address_2', models.CharField(blank=True, max_length=100, null=True)),
                ('city_town', models.CharField(blank=True, max_length=20, null=True)),
                ('county_area', models.CharField(blank=True, max_length=20, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
