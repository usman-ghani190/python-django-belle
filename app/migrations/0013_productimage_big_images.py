# Generated by Django 5.1.2 on 2024-11-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_product_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='big_images',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]