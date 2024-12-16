from django.contrib import admin

from app.models import Brand, Cart, Category, Color, Product, ProductBigImage, ProductImage, Size, SliderImages, Tag

# Register your models here.
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductImage)
admin.site.register(SliderImages)
admin.site.register(ProductBigImage)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Tag)
admin.site.register(Cart)