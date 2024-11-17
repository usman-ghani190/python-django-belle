from django.core.management.base import BaseCommand
from app.models import ProductBigImage
from PIL import Image

class Command(BaseCommand):
    help = 'Update width and height for all ProductBigImage instances'

    def handle(self, *args, **kwargs):
        for image_instance in ProductBigImage.objects.all():
            if image_instance.image:
                img = Image.open(image_instance.image)
                image_instance.width, image_instance.height = img.size
                image_instance.save()
                self.stdout.write(f"Updated: {image_instance.image.name} ({image_instance.width}x{image_instance.height})")
