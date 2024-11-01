from django.contrib import admin

from app.models import Color, Product, ProductImage, Size

# Register your models here.
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductImage)
