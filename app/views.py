from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse


from app.forms import OrderItemForm, ProductQueryAskForm
from app.models import Cart, Color, Order, OrderItem, Product, ProductBigImage, ProductImage, SliderImages

# Create your views here.
def index(request, slug=None):
    
    slider = SliderImages.objects.all()
    
    if slug:
        # If slug is provided, filter the product by slug
        products = get_object_or_404(Product, slug=slug)
        variants = ProductImage.objects.filter(product=products)
        context = {'slider': slider, 'products': products, 'stars': range(5), 'variants':variants}
    else:
        # If no slug is provided, return all products (or a default set)
        products = Product.objects.filter(is_featured=True)[:6]
        products = Product.objects.filter(is_new=True)[:4]

        variants= ProductImage.objects.all()  # Or adjust this to show a default set
        context = {'slider': slider, 'products': products, 'stars': range(5), 'variants':variants}
    
    
    return render(request, 'app/index.html', context)

def shop_page(request):
    context= {}
    return render(request, 'app/shop.html', context)

# def product_page(request, slug):
#     product = Product.objects.get(slug=slug)
   
    
#     context= {'product':product}
#     return render(request, 'app/product_page.html', context)

# def product_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = ProductImage.objects.all()
    big_variants = ProductBigImage.objects.all()

    # Calculate savings
    you_saved, percentage_saved = None, None
    if product.price and product.discounted_price:
        you_saved = product.price - product.discounted_price
        percentage_saved = (you_saved / product.price) * 100

    # Form handling
    if request.method == 'POST':
        form = ProductQueryAskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your query has been submitted successfully!")
            form = ProductQueryAskForm()

            return redirect('product', slug=slug)
        else:
            messages.error(request, "There was an error submitting your query. Please correct the form.")

    else:
        form = ProductQueryAskForm()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
        
        if action == 'add_to_cart':
            return add_to_cart(request, product, quantity)
        elif action == 'buy_now':
            return buy_now(request, product, quantity)

    # Context for the template
    context = {
        'product': product,
        'variants': variants,
        'big_variants': big_variants,
        'you_saved': you_saved,
        'percentage_saved': percentage_saved,
        'form': form,
    }
    return render(request, 'app/product_page.html', context)

def product_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = ProductImage.objects.all()
    big_variants = ProductBigImage.objects.all()

    # Calculate savings
    you_saved, percentage_saved = None, None
    if product.price and product.discounted_price:
        you_saved = product.price - product.discounted_price
        percentage_saved = (you_saved / product.price) * 100

    # Form handling for ProductQueryAskForm
    form = ProductQueryAskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Your query has been submitted successfully!")
        return redirect('product', slug=slug)
    elif request.method == 'POST':
        messages.error(request, "There was an error submitting your query. Please correct the form.")

    # Handle Add to Cart and Buy Now actions
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

        if action == 'add_to_cart':
            return add_to_cart(request, product, quantity)
        elif action == 'buy_now':
            return buy_now(request, product, quantity)

    # Context for the template
    context = {
        'product': product,
        'variants': variants,
        'big_variants': big_variants,
        'you_saved': you_saved,
        'percentage_saved': percentage_saved,
        'form': form,
    }

    return render(request, 'app/product_page.html', context)


def cart_page(request):
    
    context= {}
    return render(request, 'app/cart.html', context)



def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        color = request.POST.get('option-0')
        size = request.POST.get('option-1')
        quantity = request.POST.get('quantity')
        
        # Add to the user's cart logic here, e.g., saving to session or database
        
        return HttpResponseRedirect('/cart/')  # Redirect to the cart page after adding the product
    
    colors = product.available_colors.all()
    sizes = product.available_sizes.all()
    
    context = {
        'product': product,
        'colors': colors,
        'sizes': sizes,
    }
    return render(request, 'app/cart.html', context)


def listview(request):
    context= {}
    return render(request, 'app/shop_listview.html', context)

def login_page(request):
    context= {}
    return render(request, 'app/login.html', context)

def register_page(request):
    context= {}
    return render(request, 'app/register.html', context)

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    colors = product.available_colors.all()  # Fetching the available colors for the product
    sizes = product.available_sizes.all()  # Fetching the available sizes for the product
    
    context = {
        'product': product,
        'colors': colors,  # Passing colors to the template
        'sizes': sizes,    # Passing sizes to the template
    }
    return render(request, 'app/checkout.html', context)  



def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Logic to create an order and redirect to the checkout page
    return redirect('checkout')

def wishlist(request, slug):

    context={}
    return render(request, 'app/wishlist.html', context)