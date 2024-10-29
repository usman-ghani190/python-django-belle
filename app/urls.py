

from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop_page, name='shop'),
    path('shop/product', views.product_page, name='product'),
    path('shop/cart', views.cart_page, name='cart'),

]
