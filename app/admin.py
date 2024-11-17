from django.contrib import admin

from app.models import Color, Product, ProductBigImage, ProductImage, Size, SliderImages

# Register your models here.
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductImage)
admin.site.register(SliderImages)
admin.site.register(ProductBigImage)
