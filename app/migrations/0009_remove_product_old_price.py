# Generated by Django 5.1.2 on 2024-11-12 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_product_old_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
    ]
