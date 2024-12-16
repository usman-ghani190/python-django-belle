from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse



from app.forms import OrderItemForm, ProductQueryAskForm, ReviewForm
from app.models import Brand, Cart, CartItem, Category, Color, Order, OrderItem, Product, ProductBigImage, ProductImage, Size, SliderImages, Tag

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
    categories = Category.objects.filter(parent__isnull=True)
    products = Product.objects.all()
    colors= Color.objects.all()
    sizes = Size.objects.all()
    brands= Brand.objects.all()
    tags= Tag.objects.all()
    selected_size = request.GET.get('size') 

    if selected_size:
        # Filter products that have the selected size
        products = products.filter(available_sizes__name=selected_size)

    # Get the min and max price from the query parameters
    price = request.GET.get('amount')

    # Filter products based on the price range
    if price:
        products = products.filter(price__lte=price)

     # Get the selected sorting option from GET parameters
    sort_option = request.GET.get('SortBy', 'title-ascending')
    if sort_option == 'best-selling':
        products = products.order_by('-is_on_sale')  # Example: Sort by sales
    elif sort_option == 'alphabetically-az':
        products = products.order_by('name')
    elif sort_option == 'alphabetically-za':
        products = products.order_by('-name')
    elif sort_option == 'price-low-high':
        products = products.order_by('price')
    elif sort_option == 'price-high-low':
        products = products.order_by('-price')
    elif sort_option == 'discounted':
        products = products.order_by('-discounted_price')
    elif sort_option == 'non-discounted':
        products = products.order_by('discounted_price')

    # Get the total number of products after filtering
    product_count = products.count()

    context = {
        "categories": categories,
        "products": products,
        'colors':colors,
        'sizes':sizes,
        'brands':brands,
        'tags':tags,
        'selected_size': selected_size,
        'sort_option': sort_option,
        'product_count': product_count,
    }
    return render(request, 'app/shop.html', context)


def product_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = ProductImage.objects.all()
    big_variants = ProductBigImage.objects.all()
    reviews = product.reviews.all()  # Fetch all reviews for the product
    related_products = Product.objects.exclude(id=product.id)[:4]

     # Fetch recently viewed products from session
    recently_viewed = request.session.get('recently_viewed', [])
    if product.id not in recently_viewed:
        recently_viewed.append(product.id)
        # Limit the number of stored products (e.g., 5)
        if len(recently_viewed) > 5:
            recently_viewed.pop(0)
    request.session['recently_viewed'] = recently_viewed

    # Calculate savings
    you_saved, percentage_saved = None, None
    if product.price and product.discounted_price:
        you_saved = product.price - product.discounted_price
        percentage_saved = (you_saved / product.price) * 100

    # Handle ReviewForm submission
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            # Save the form data and associate with the product
            review = review_form.save(commit=False)
            review.product = product  # Link the review to the product
            review.save()  # Save the review to the database
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('product', slug=slug)  # Redirect to avoid form resubmission
        else:
            messages.error(request, "There was an error submitting your review. Please correct the form.")

    # Handle ProductQueryAskForm submission (untouched logic)
    form = ProductQueryAskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and 'query_submit' in request.POST:
        form.save()
        messages.success(request, "Your query has been submitted successfully!")
        return redirect('product', slug=slug)
    
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
        'reviews': reviews,
        'review_form': review_form,
        'form': form,
        'related_products':related_products,
        
    }

    return render(request, 'app/product_page.html', context)




def add_to_cart(request, product, quantity):
    color_name = request.POST.get('option-0')
    size_name = request.POST.get('option-1')

    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    color = get_object_or_404(Color, name=color_name)
    size = get_object_or_404(Size, name=size_name)

    if request.user.is_authenticated:
        # Use the user for authenticated users
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Use the session key for anonymous users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Create a session if none exists
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
    cart_item.quantity = int(quantity)
    cart_item.save()

    messages.success(request, "Item added to cart!")
    return redirect(reverse('cart'))


# def cart_page(request):
    
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         session_key = request.session.session_key
#         if not session_key:
#             request.session.create()
#             session_key = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_key=session_key)

#     if request.method == 'POST':
#             note = request.POST.get('note')
#             terms_agreed = request.POST.get('tearm')  # Handling the terms and conditions checkbox
#             cart.note = note
#             cart.terms_agreed = terms_agreed
#             cart.save()

#             if 'checkout' in request.POST and terms_agreed:
#                 # Handle checkout logic here (e.g., create an order)
#                 return HttpResponseRedirect('/checkout/')  # Redirect to checkout page


#     if request.method == 'POST':
#             if 'update_quantity' in request.POST:  # Quantity update logic
#                 item_id = request.POST.get('item_id')
#                 new_quantity = int(request.POST.get('quantity', 1))
#                 cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
#                 cart_item.quantity = max(1, new_quantity)  # Avoid zero/negative quantities
#                 cart_item.save()
#                 return JsonResponse({
#                     'total_price': cart_item.product.price * cart_item.quantity,
#                     'subtotal': sum(i.product.price * i.quantity for i in cart.cartitem_set.all())
#                 })
#             # Remove item logic
#             if request.method == 'GET':
#                 if 'remove_item' in request.GET:
#                     item_id = request.GET.get('remove_item')
#                     if item_id:
#                         cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#                         if cart_item:
#                             cart_item.delete()
#                             messages.success(request, "Item removed from cart.")
#                         else:
#                             messages.error(request, "Item not found in cart.")
#                     else:
#                         messages.error(request, "Item ID not provided.")
#                     return redirect('cart')

    

#     cart_items = cart.cartitem_set.all()

#     # Calculate the total price for each item in the cart
#     for item in cart_items:
#         item.total_price = item.product.price * item.quantity
#     subtotal = sum(item.product.price * item.quantity for item in cart_items)
#     # Calculate the grand total for the cart
#     # total = sum(item.total_price for item in cart_items)

#     context = {
#         'cart': cart,
#         'cart_items': cart_items,
#         'subtotal':subtotal,
        
#     }

#     return render(request, 'app/cart.html', context)

def cart_page(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    if request.method == 'POST':
        # Handle the 'note' and 'terms_agreed' in POST
        note = request.POST.get('note')
        terms_agreed = request.POST.get('tearm')  # Handling the terms and conditions checkbox
        cart.note = note
        cart.terms_agreed = terms_agreed
        cart.save()

        if 'checkout' in request.POST and terms_agreed:
            # Handle checkout logic here (e.g., create an order)
            return HttpResponseRedirect('/checkout/')  # Redirect to checkout page

        if 'update_quantity' in request.POST:  # Quantity update logic
            item_id = request.POST.get('item_id')
            new_quantity = int(request.POST.get('quantity', 1))
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.quantity = max(1, new_quantity)  # Avoid zero/negative quantities
            cart_item.save()
            return JsonResponse({
                'total_price': cart_item.product.price * cart_item.quantity,
                'subtotal': sum(i.product.price * i.quantity for i in cart.cartitem_set.all())
            })

    elif request.method == 'GET':
        if 'remove_item' in request.GET:
            item_id = request.GET.get('remove_item')
            if item_id:
                cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
                if cart_item:
                    cart_item.delete()
                    messages.success(request, "Item removed from cart.")
                else:
                    messages.error(request, "Item not found in cart.")
            else:
                messages.error(request, "Item ID not provided.")
            return redirect('cart')  # Redirect to cart page after removal

    cart_items = cart.cartitem_set.all()

    # Calculate the total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
    }

    return render(request, 'app/cart.html', context)





# def cart_page(request):
#     if request.user.is_authenticated:
#         # Use the user to fetch or create the cart for authenticated users
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         # Use the session key for anonymous users
#         session_key = request.session.session_key
#         if not session_key:
#             request.session.create()  # Create a session if none exists
#             session_key = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_key=session_key)

#     # Fetch the cart items
#     cart_items = cart.cartitem_set.all()

#     context = {
#         'cart': cart,
#         'cart_items': cart_items,
#     }
#     return render(request, 'app/cart.html', context)





def buy_now(request, product, quantity):
    color_name = request.POST.get('option-0')
    size_name = request.POST.get('option-1')

    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    color = get_object_or_404(Color, name=color_name)
    size = get_object_or_404(Size, name=size_name)

    # Handle carts for both authenticated and anonymous users
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Use session key for anonymous users
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
    cart_item.quantity += int(quantity)
    cart_item.save()

    return redirect(reverse('checkout'))




def checkout(request):
    # Fetch all cart items for the current user or session
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    if not cart:
        messages.error(request, "Your cart is empty.")
        return HttpResponseRedirect('/shop/')

    cart_items = cart.cartitem_set.all()

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'app/checkout.html', context)



def listview(request):
    context= {}
    return render(request, 'app/shop_listview.html', context)

def login_page(request):
    context= {}
    return render(request, 'app/login.html', context)

def register_page(request):
    context= {}
    return render(request, 'app/register.html', context)




def wishlist(request, slug):
    product= get_object_or_404(Product, slug=slug)

    context={'product':product }
    return render(request, 'app/wishlist.html', context)