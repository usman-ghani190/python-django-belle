# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from .models import Cart, CartItem

# @receiver(user_logged_in)
# def merge_carts_on_login(sender, request, user, **kwargs):
#     # Check if a session-based cart exists
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.create()
#         session_key = request.session.session_key

#     session_cart = Cart.objects.filter(session_key=session_key).first()
#     user_cart = Cart.objects.filter(user=user).first()

#     if session_cart:
#         if user_cart:
#             # Merge session cart items into user cart
#             session_cart_items = CartItem.objects.filter(cart=session_cart)
#             for item in session_cart_items:
#                 # Check if the item already exists in the user's cart
#                 user_cart_item = CartItem.objects.filter(
#                     cart=user_cart, product=item.product, color=item.color, size=item.size
#                 ).first()
#                 if user_cart_item:
#                     user_cart_item.quantity += item.quantity
#                     user_cart_item.save()
#                 else:
#                     # Move the item to the user cart
#                     item.cart = user_cart
#                     item.save()
#             # Delete the session-based cart
#             session_cart.delete()
#         else:
#             # If no user cart exists, assign the session cart to the user
#             session_cart.user = user
#             session_cart.session_key = None  # Clear session key for this cart
#             session_cart.save()
