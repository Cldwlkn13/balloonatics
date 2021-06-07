# Generated by Django 3.2.3 on 2021-06-07 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20210607_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_id', models.CharField(editable=False, max_length=56, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='bundleitem',
            name='bundle_item_id',
        ),
        migrations.RemoveField(
            model_name='bundleitem',
            name='bundle_item_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_bundle',
        ),
        migrations.AlterField(
            model_name='bundleitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='bundleitem',
            name='bundle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bundle_items', to='products.bundle'),
        ),
    ]