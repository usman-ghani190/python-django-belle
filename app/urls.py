

from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('shop/', views.shop_page, name='shop'),
    path('shop/product', views.product_page, name='product'),
    path('shop/cart', views.cart_page, name='cart'),
    path('shop/list_view', views.listview, name='listview'),


]
