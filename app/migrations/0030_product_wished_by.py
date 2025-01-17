# Generated by Django 5.1.2 on 2025-01-05 19:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_register'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='wished_by',
            field=models.ManyToManyField(blank=True, related_name='wishlisted_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
