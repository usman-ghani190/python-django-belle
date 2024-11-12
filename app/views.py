from django.shortcuts import get_object_or_404, redirect, render

from app.forms import OrderItemForm
from app.models import Color, OrderItem, Product, SliderImages

# Create your views here.
def index(request):
    slider= SliderImages.objects.all()
    product= Product.objects.get()
    rating= product.rating

    context= {'slider':slider, 'product':product, 'rating':rating, 'stars': range(5),}
    return render(request, 'app/index.html', context)

def shop_page(request):
    context= {}
    return render(request, 'app/shop.html', context)

# def product_page(request, slug):
#     product = Product.objects.get(slug=slug)
   
    
#     context= {'product':product}
#     return render(request, 'app/product_page.html', context)

def product_page(request, ):
    
    product = Product.objects.get()

    context= {'product':product}
    return render(request, 'app/product_page.html', context)

def cart_page(request):
    context= {}
    return render(request, 'app/cart.html', context)

def add_to_cart(request, slug):
    # Retrieve the product based on the slug
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        # Retrieve the quantity from the hidden form field
        quantity = int(request.POST.get('quantity', 1))  # Defaults to 1 if not set
        order_item, created = OrderItem.objects.get_or_create(
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            # If the item is already in the cart, update its quantity
            order_item.quantity += quantity
            order_item.save()

        return redirect('cart')  # Redirect to the cart page or desired page

    return render(request, 'app/product_page.html', {'product': product})

def listview(request):
    context= {}
    return render(request, 'app/shop_listview.html', context)

def login_page(request):
    context= {}
    return render(request, 'app/login.html', context)

def register_page(request):
    context= {}
    return render(request, 'app/register.html', context)

def checkout(request):
    context= {}
    return render(request, 'app/checkout.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Add product to cart logic here
    return redirect('cart')

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Logic to create an order and redirect to the checkout page
    return redirect('checkout')
