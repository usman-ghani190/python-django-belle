import django.db.models.deletion
from django.db import migrations, models

from app.models import CartItem


def set_default_values(apps, schema_editor):
    Color = apps.get_model('app', 'Color')
    Size = apps.get_model('app', 'Size')

    # Fetch default color and size objects (make sure they exist in the database)
    default_color = Color.objects.get(name='Red')  # Assuming 'Red' is a valid color
    default_size = Size.objects.get(name='M')  # Assuming 'M' is a valid size

    # Set default color and size for all CartItem rows that currently have NULL values
    CartItem.objects.filter(color__isnull=True).update(color=default_color)
    CartItem.objects.filter(size__isnull=True).update(size=default_size)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_cart_cartitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.color'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.size'),
        ),
    ]
