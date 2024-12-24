from .models import Cart, CartItem

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

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
