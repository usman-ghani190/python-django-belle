from django.shortcuts import get_object_or_404, redirect, render

from app.forms import OrderItemForm
from app.models import Color, OrderItem, Product, ProductBigImage, ProductImage, SliderImages

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

def product_page(request, slug):
    
    product = get_object_or_404(Product, slug=slug)
    
    variants= ProductImage.objects.all()  # Or adjust this to show a default set
    big_variants= ProductBigImage.objects.all()

    if product.price and product.discounted_price:
        you_saved = product.price - product.discounted_price
        # Calculate the percentage savings
        percentage_saved = (you_saved / product.price) * 100
    else:
        you_saved = None
        percentage_saved = None

    context= {'product':product, 'variants':variants, 'big_variants':big_variants, 'you_saved':you_saved, 'percentage_saved':percentage_saved}
    return render(request, 'app/product_page.html', context)

def cart_page(request):
    context= {}
    return render(request, 'app/cart.html', context)

def add_to_cart(request, slug):
    # Retrieve the product based on the slug
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        # Retrieve the quantity from the form, with a default value of 1 if not set
        quantity = int(request.POST.get('quantity', 1))  # Defaults to 1 if not set

        # Make sure quantity is a positive integer
        if quantity <= 0:
            # Handle invalid quantity (optional: could be an error message)
            return redirect('product', slug=slug)  # Redirect back to the product page

        # Get or create the order item
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

def wishlist(request, slug):

    context={}
    return render(request, 'app/wishlist.html', context)