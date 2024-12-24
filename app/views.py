from decimal import Decimal
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse



from app.forms import CheckoutForm, OrderItemForm, PaymentForm, ProductQueryAskForm, ReviewForm
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
        

    cart = request.session.get('cart', {})  # Get cart from session
    product_quantity = cart.get(str(product.id), 1)  # Default to 1 if not in cart




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
        'product_quantity':product_quantity,
        
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
#         session_key = request.session.session_key or request.session.create()
#         cart, created = Cart.objects.get_or_create(session_key=session_key)

#     # Handle Quantity Updates via POST (AJAX)
#     if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         item_id = request.POST.get('id')
#         quantity = request.POST.get('quantity')

#         if not item_id or not quantity:
#             return JsonResponse({'success': False, 'error': 'Missing item ID or quantity'}, status=400)

#         try:
#             quantity = int(quantity)
#             if quantity <= 0:
#                 return JsonResponse({'success': False, 'error': 'Quantity must be greater than zero'}, status=400)

#             # Check if item_id belongs to a product or a CartItem
#             if CartItem.objects.filter(id=item_id, cart=cart).exists():
#                 cart_item = CartItem.objects.get(id=item_id, cart=cart)
#             else:
#                 # Handle case for product page
#                 product = get_object_or_404(Product, id=item_id)
#                 cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
#             # Update the quantity
#             cart_item.quantity = quantity
#             cart_item.save()

#             # Calculate the subtotal dynamically
#             subtotal = sum(item.total_price for item in cart.cartitem_set.all())
#             response_data = {
#                 'success': True,
#                 'cart_items': [
#                     {
#                         'id': item.id,
#                         'total_price': float(item.total_price),
#                         'quantity': item.quantity,
#                         'product': {
#                             'name': item.product.name,
#                             'image_url': item.product.main_image.url if item.product.main_image else '/static/images/default-product.jpg',
#                             'color': item.color.name if item.color else '',
#                             'size': item.size.name if item.size else '',
#                         },
#                     }
#                     for item in cart.cartitem_set.all()
#                 ],
#                 'subtotal': float(subtotal),
#             }
#             return JsonResponse(response_data)

#         except ValueError:
#             return JsonResponse({'success': False, 'error': 'Invalid quantity value'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)
        
#         # Handle item removal
#     if 'remove_item' in request.GET:
#         item_id = request.GET.get('remove_item')
#         cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#         if cart_item:
#             cart_item.delete()
#             messages.success(request, "Item removed from cart.")
#         else:
#             messages.error(request, "Item not found in cart.")
#         return redirect('cart')

#     # Fetch cart items and calculate totals dynamically
#     cart_items = cart.cartitem_set.all()
#     subtotal = sum(item.total_price for item in cart.cartitem_set.all())

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#     }
#     return render(request, 'app/cart.html', context)

# def cart_page(request):
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         session_key = request.session.session_key or request.session.create()
#         cart, created = Cart.objects.get_or_create(session_key=session_key)

#     # Handle Quantity Updates or Item Removal via POST (AJAX)
#     if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         item_id = request.POST.get('id')
#         action = request.POST.get('action')  # New 'action' field to differentiate between update and remove
#         quantity = request.POST.get('quantity')

#         # Handle item removal
#         if action == 'remove':
#             if not item_id:
#                 return JsonResponse({'success': False, 'error': 'Missing item ID'}, status=400)

#             cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#             if cart_item:
#                 cart_item.delete()
                
#                 # Recalculate the subtotal dynamically
#                 subtotal = sum(item.total_price for item in cart.cartitem_set.all())
#                 response_data = {
#                     'success': True,
#                     'cart_items': [
#                         {
#                             'id': item.id,
#                             'total_price': float(item.total_price),
#                             'quantity': item.quantity,
#                             'product': {
#                                 'name': item.product.name,
#                                 'image_url': item.product.main_image.url if item.product.main_image else '/static/images/default-product.jpg',
#                                 'color': item.color.name if item.color else '',
#                                 'size': item.size.name if item.size else '',
#                             },
#                         }
#                         for item in cart.cartitem_set.all()
#                     ],
#                     'subtotal': float(subtotal),
#                 }
#                 return JsonResponse(response_data)
#             else:
#                 return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

#         # Handle quantity update
#         if not item_id or not quantity:
#             return JsonResponse({'success': False, 'error': 'Missing item ID or quantity'}, status=400)

#         try:
#             quantity = int(quantity)
#             if quantity <= 0:
#                 return JsonResponse({'success': False, 'error': 'Quantity must be greater than zero'}, status=400)

#             # Check if item_id belongs to a product or a CartItem
#             if CartItem.objects.filter(id=item_id, cart=cart).exists():
#                 cart_item = CartItem.objects.get(id=item_id, cart=cart)
#             else:
#                 # Handle case for product page
#                 product = get_object_or_404(Product, id=item_id)
#                 cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            
#             # Update the quantity
#             cart_item.quantity = quantity
#             cart_item.save()

#             # Calculate the subtotal dynamically
#             subtotal = sum(item.total_price for item in cart.cartitem_set.all())
#             response_data = {
#                 'success': True,
#                 'cart_items': [
#                     {
#                         'id': item.id,
#                         'total_price': float(item.total_price),
#                         'quantity': item.quantity,
#                         'product': {
#                             'name': item.product.name,
#                             'image_url': item.product.main_image.url if item.product.main_image else '/static/images/default-product.jpg',
#                             'color': item.color.name if item.color else '',
#                             'size': item.size.name if item.size else '',
#                         },
#                     }
#                     for item in cart.cartitem_set.all()
#                 ],
#                 'subtotal': float(subtotal),
#             }
#             return JsonResponse(response_data)

#         except ValueError:
#             return JsonResponse({'success': False, 'error': 'Invalid quantity value'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)

#     # Handle item removal from the cart using a GET request (if needed for non-AJAX removal)
#     if 'remove_item' in request.GET:
#         item_id = request.GET.get('remove_item')
#         cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#         if cart_item:
#             cart_item.delete()
#             messages.success(request, "Item removed from cart.")
#         else:
#             messages.error(request, "Item not found in cart.")
#         return redirect('cart')

#     # Fetch cart items and calculate totals dynamically
#     cart_items = cart.cartitem_set.all()
#     subtotal = sum(item.total_price for item in cart.cartitem_set.all())

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#     }
#     return render(request, 'app/cart.html', context)


# def cart_page(request):
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         session_key = request.session.session_key or request.session.create()
#         cart, created = Cart.objects.get_or_create(session_key=session_key)

#     # Handle Quantity Updates and Item Removal via POST (AJAX)
#     if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         item_id = request.POST.get('id')
#         action = request.POST.get('action', None)
#         quantity = request.POST.get('quantity', None)

#         if not item_id:
#             return JsonResponse({'success': False, 'error': 'Missing item ID'}, status=400)

#         try:
#             # Handle item removal
#             if action == "remove":
#                 cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#                 if cart_item:
#                     cart_item.delete()
#                     # Calculate updated subtotal
#                     subtotal = sum(item.total_price for item in cart.cartitem_set.all())
#                     response_data = {
#                         'success': True,
#                         'cart_items': [
#                             {
#                                 'id': item.id,
#                                 'product': {
#                                     'name': item.product.name,
#                                     'image_url': item.product.main_image.url if item.product.main_image else None,
#                                     'color': item.color.name if item.color else None,
#                                     'size': item.size.name if item.size else None,
#                                 },
#                                 'total_price': float(item.total_price),
#                                 'quantity': item.quantity,
#                             }
#                             for item in cart.cartitem_set.all()
#                         ],
#                         'subtotal': float(subtotal),
#                     }
#                     return JsonResponse(response_data)
#                 else:
#                     return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

#             # Handle quantity update
#             if quantity:
#                 quantity = int(quantity)
#                 if quantity <= 0:
#                     return JsonResponse({'success': False, 'error': 'Quantity must be greater than zero'}, status=400)

#                 # Check if item_id belongs to a CartItem
#                 cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#                 if cart_item:
#                     cart_item.quantity = quantity
#                     cart_item.save()

#                     # Calculate updated subtotal
#                     subtotal = sum(item.total_price for item in cart.cartitem_set.all())
#                     response_data = {
#                         'success': True,
#                         'cart_items': [
#                             {
#                                 'id': item.id,
#                                 'product': {
#                                     'name': item.product.name,
#                                     'image_url': item.product.main_image.url if item.product.main_image else None,
#                                     'color': item.color.name if item.color else None,
#                                     'size': item.size.name if item.size else None,
#                                 },
#                                 'total_price': float(item.total_price),
#                                 'quantity': item.quantity,
#                             }
#                             for item in cart.cartitem_set.all()
#                         ],
#                         'subtotal': float(subtotal),
#                     }
#                     return JsonResponse(response_data)

#             return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

#         except ValueError:
#             return JsonResponse({'success': False, 'error': 'Invalid quantity value'}, status=400)
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)}, status=500)

#     # Fetch cart items and calculate totals dynamically
#     cart_items = cart.cartitem_set.all()
#     subtotal = sum(item.total_price for item in cart.cartitem_set.all())

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#     }
#     return render(request, 'app/cart.html', context)


def cart_page(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    # Handle Quantity Updates and Item Removal via POST (AJAX)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        item_id = request.POST.get('id')
        action = request.POST.get('action', None)
        quantity = request.POST.get('quantity', None)

        if not item_id:
            return JsonResponse({'success': False, 'error': 'Missing item ID'}, status=400)

        try:
            # Handle item removal
            if action == "remove":
                cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
                if cart_item:
                    cart_item.delete()

            # Handle quantity update
            if quantity:
                quantity = int(quantity)
                if quantity <= 0:
                    return JsonResponse({'success': False, 'error': 'Quantity must be greater than zero'}, status=400)

                # Check if item_id belongs to a CartItem
                cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
                if cart_item:
                    cart_item.quantity = quantity
                    cart_item.save()

            # Calculate updated subtotal
            cart_items = cart.cartitem_set.all()
            subtotal = sum(item.total_price for item in cart_items)

            response_data = {
                'success': True,
                'cart_items': [
                    {
                        'id': item.id,
                        'quantity': item.quantity,
                        'total_price': float(item.total_price),
                        'product': {
                            'name': item.product.name,
                            'image_url': item.product.main_image.url if item.product.main_image else None,
                            'color': item.color.name if item.color else None,
                            'size': item.size.name if item.size else None,
                            'price': float(item.product.price),
                        }
                    }
                    for item in cart_items
                ],
                'subtotal': float(subtotal),
            }
            return JsonResponse(response_data)

        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid quantity value'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        
    # Handle item removal
    if 'remove_item' in request.GET:
        item_id = request.GET.get('remove_item')
        cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
        if cart_item:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
        else:
            messages.error(request, "Item not found in cart.")
        return redirect('cart')

    # Fetch cart items and calculate totals dynamically
    cart_items = cart.cartitem_set.all()
    subtotal = sum(item.total_price for item in cart.cartitem_set.all())

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }
    return render(request, 'app/cart.html', context)










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

    # Initialize forms
    checkout_form = CheckoutForm()
    payment_form = PaymentForm()

    # Handle POST request for CheckoutForm
    if request.method == request.POST:
        checkout_form = CheckoutForm(request.POST)
        if checkout_form.is_valid():
            checkout_form.save()
            messages.success(request, "Billing details saved successfully!")
            return redirect("checkout")  # Redirect to refresh the page
        else:
            messages.error(request, "Please correct the errors in the billing form.")

    # Handle POST request for PaymentForm
    elif request.method ==  request.POST:
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, "Payment completed successfully!")
            return redirect("success")  # Redirect to a success page
        else:
            messages.error(request, "Please correct the errors in the payment form.")

    # Calculate totals
    cart_items = cart.cartitem_set.all()
    subtotal = sum(item.total_price for item in cart_items)
    shipping_cost = Decimal("50.00")  # Example shipping cost
    total_cost = subtotal + shipping_cost

    context = {
        "cart_items": cart_items,
        "checkout_form": checkout_form,
        "payment_form": payment_form,
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "total_cost": total_cost,
    }
    return render(request, "app/checkout.html", context)


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


def thank_you(request):
    
    context={}

    return render(request, 'app/thanks.html', context)