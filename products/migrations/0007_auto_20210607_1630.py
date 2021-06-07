# Generated by Django 3.2.3 on 2021-06-07 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_qty_in_bag'),
    ]

    operations = [
        migrations.CreateModel(
            name='BundleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='bundle_items',
            field=models.ManyToManyField(to='products.BundleItem'),
        ),
    ]
