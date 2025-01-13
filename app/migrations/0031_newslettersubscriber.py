# Generated by Django 5.1.2 on 2025-01-12 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_product_wished_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_subscribed', models.BooleanField(default=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
                ('unsubscribed_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]