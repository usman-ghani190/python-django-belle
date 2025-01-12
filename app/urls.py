

from . import views
from django.urls import include, path


urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.index, name='index_with_slug'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('shop/', include([
        path('', views.shop_page, name='shop'),
        path('product/<slug:slug>/', views.product_page, name='product'),
        path('cart/', views.cart_page, name='cart'),
        path('list_view/', views.listview, name='listview'),
        path('cart/add/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
        path('cart/add/<slug:slug>/wishlist_item/<int:wishlist_item_id>/', views.add_to_cart, name='add_to_cart_from_wishlist'),
        path('wishlist/', views.wishlist_view, name='wishlist'),
        path('wishlist/add/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
        path('wishlist/remove/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
        path('checkout/', views.checkout, name='checkout'),
        path('thank_you',views.thank_you, name='thank_you' )
    ])),
    path('shop/checkout/', views.checkout, name='checkout'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('logout/', views.logout_view, name='logout'),

]

