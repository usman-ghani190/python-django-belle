# app/context_processors.py

from .models import Cart, CartItem

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.cartitem_set.all()
            subtotal = sum(item.total_price for item in cart_items)
            total_items = sum(item.quantity for item in cart_items)
        else:
            cart_items = []
            subtotal = 0
            total_items = 0
        
        return {
            'cart_items': cart_items,
            'cart_subtotal': subtotal,
            'cart_total_items': total_items,
        }
    
    # For anonymous users, return empty cart data without accessing request.session
    return {
        'cart_items': [],
        'cart_subtotal': 0,
        'cart_total_items': 0,
    }
