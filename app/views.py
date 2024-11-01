from django.shortcuts import get_object_or_404, redirect, render

from app.forms import OrderItemForm
from app.models import Color, Product

# Create your views here.
def index(request):
    context= {}
    return render(request, 'app/index.html', context)

def shop_page(request):
    context= {}
    return render(request, 'app/shop.html', context)

# def product_page(request, slug):
#     product = Product.objects.get(slug=slug)
   
    
#     context= {'product':product}
#     return render(request, 'app/product_page.html', context)

def product_page(request):
    product = Product.objects.get()

    context= {'product':product}
    return render(request, 'app/product_page.html', context)

def cart_page(request):
    context= {}
    return render(request, 'app/cart.html', context)

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=product.objects.get('slug'))

    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.product = product
            order_item.save()
            return redirect('cart')  # or any other page you want to redirect to
    else:
        form = OrderItemForm()

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'app/product_page.html', context)



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
