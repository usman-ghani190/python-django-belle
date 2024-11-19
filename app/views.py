from venv import logger
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse



from app.forms import OrderItemForm, ProductQueryAskForm
from app.models import Cart, CartItem, Color, Order, OrderItem, Product, ProductBigImage, ProductImage, Size, SliderImages

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

# def add_to_cart(request, product, quantity):

    print(f"POST data: {request.POST}")

    # Get the selected color and size from the form
    color_name = request.POST.get('option-0')  # This is the color
    size_name = request.POST.get('option-1')   # This is the size

    print(f"Selected color: {color_name}, Selected size: {size_name}")

    # Ensure color and size are selected
    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Go back to the product page if not selected
    
    # Get the color and size objects
    color = get_object_or_404(Product.available_colors.through, product=product, color__name=color_name).color
    size = get_object_or_404(Product.available_sizes.through, product=product, size=size_name).size
    
    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the item already exists in the cart (same product, color, and size)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
    
    # Update the quantity if the item already exists in the cart
    cart_item.quantity += int(quantity)
    cart_item.save()

    print("Redirecting to cart...")
    
    # Redirect to the cart page
    return HttpResponseRedirect(reverse('cart'))

def add_to_cart(request, product, quantity):
    # Get the selected color and size from the form
    color_name = request.POST.get('option-0')  # This is the color
    size_name = request.POST.get('option-1')   # This is the size
    
    print(f"Selected color: {color_name}, Selected size: {size_name}")

    # Ensure color and size are selected
    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Go back to the product page if not selected
    
    # Get the color and size objects by their name
    color = get_object_or_404(Color, name=color_name)
    size = get_object_or_404(Size, name=size_name)
    
    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the item already exists in the cart (same product, color, and size)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
    
    # Update the quantity if the item already exists in the cart
    cart_item.quantity += int(quantity)
    cart_item.save()

    print("Redirecting to cart...")
    
    # Redirect to the cart page
    return HttpResponseRedirect(reverse('cart'))



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
    # Assuming you have a Cart model to fetch cart items for the user
    cart = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,  # Pass cart to the template
    }
    return render(request, 'app/cart.html', context)




# def add_to_cart(request, slug):
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

# def add_to_cart(request, product, quantity):
    # Assuming you have a Cart model and CartItem model

    cart, created = Cart.objects.get_or_create(user=request.user)  # You may need to customize this based on your cart model

    # Logic to add the product to the cart
    cart.add_item(product, quantity)  # Implement add_item in the Cart model

    # Redirect to cart page
    return HttpResponseRedirect(reverse('cart'))

    # Get the product by slug
    product = get_object_or_404(Product, slug=slug)

    # Get selected color and size
    color_name = request.POST.get('color')
    size_name = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))

    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Return to the product page if not selected

    # Get color and size objects
    color = get_object_or_404(product.available_colors, name=color_name)
    size = get_object_or_404(product.available_sizes, name=size_name)

    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)

    # Update quantity if item already exists in the cart
    cart_item.quantity += quantity
    cart_item.save()

    # Redirect to the cart page after adding the item
    return HttpResponseRedirect(reverse('cart'))

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

def buy_now(request, product, quantity):
    # Create an order for the user
    order = Order.objects.create(user=request.user, product=product, quantity=quantity)

    # Redirect to the checkout page
    return redirect('checkout', product_id=order.id)




def wishlist(request, slug):

    context={}
    return render(request, 'app/wishlist.html', context)