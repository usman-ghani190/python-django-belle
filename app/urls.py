

from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('shop/', views.shop_page, name='shop'),
    # path('shop/product/<slug:slug>/', views.product_page, name='product'),
    path('shop/product/', views.product_page, name='product'),
    path('shop/cart', views.cart_page, name='cart'),
    path('shop/list_view', views.listview, name='listview'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/buy-now/<int:product_id>/', views.buy_now, name='buy_now'),


]
