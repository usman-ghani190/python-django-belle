# from decimal import Decimal
# from django.http import HttpResponseRedirect, JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.urls import reverse
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required



# from app.forms import CheckoutForm, PaymentForm, ProductQueryAskForm, RegisterForm, ReviewForm
# from app.models import Brand, Cart, CartItem, Category, Color, Product, ProductBigImage, ProductImage, Size, SliderImages, Tag

# # Create your views here.
# def index(request, slug=None):
    
#     slider = SliderImages.objects.all()
    
#     if slug:
#         # If slug is provided, filter the product by slug
#         products = get_object_or_404(Product, slug=slug)
#         variants = ProductImage.objects.filter(product=products)
#         context = {'slider': slider, 'products': products, 'stars': range(5), 'variants':variants}
#     else:
#         # If no slug is provided, return all products (or a default set)
#         products = Product.objects.filter(is_featured=True)[:6]
#         products = Product.objects.filter(is_new=True)[:4]

#         variants= ProductImage.objects.all()  # Or adjust this to show a default set
#         context = {'slider': slider, 'products': products, 'stars': range(5), 'variants':variants}
    
    
#     return render(request, 'app/index.html', context)

# def shop_page(request):
#     categories = Category.objects.filter(parent__isnull=True)
#     products = Product.objects.all()
#     colors= Color.objects.all()
#     sizes = Size.objects.all()
#     brands= Brand.objects.all()
#     tags= Tag.objects.all()
#     selected_size = request.GET.get('size') 

#     if selected_size:
#         # Filter products that have the selected size
#         products = products.filter(available_sizes__name=selected_size)

#     # Get the min and max price from the query parameters
#     price = request.GET.get('amount')

#     # Filter products based on the price range
#     if price:
#         products = products.filter(price__lte=price)

#      # Get the selected sorting option from GET parameters
#     sort_option = request.GET.get('SortBy', 'title-ascending')
#     if sort_option == 'best-selling':
#         products = products.order_by('-is_on_sale')  # Example: Sort by sales
#     elif sort_option == 'alphabetically-az':
#         products = products.order_by('name')
#     elif sort_option == 'alphabetically-za':
#         products = products.order_by('-name')
#     elif sort_option == 'price-low-high':
#         products = products.order_by('price')
#     elif sort_option == 'price-high-low':
#         products = products.order_by('-price')
#     elif sort_option == 'discounted':
#         products = products.order_by('-discounted_price')
#     elif sort_option == 'non-discounted':
#         products = products.order_by('discounted_price')

#     # Get the total number of products after filtering
#     product_count = products.count()

#     context = {
#         "categories": categories,
#         "products": products,
#         'colors':colors,
#         'sizes':sizes,
#         'brands':brands,
#         'tags':tags,
#         'selected_size': selected_size,
#         'sort_option': sort_option,
#         'product_count': product_count,
#     }
#     return render(request, 'app/shop.html', context)


# # def product_page(request, slug):
# #     product = get_object_or_404(Product, slug=slug)
# #     variants = ProductImage.objects.all()
# #     big_variants = ProductBigImage.objects.all()
# #     reviews = product.reviews.all()  # Fetch all reviews for the product
# #     related_products = Product.objects.exclude(id=product.id)[:4]

# #      # Fetch recently viewed products from session
# #     recently_viewed = request.session.get('recently_viewed', [])
# #     if product.id not in recently_viewed:
# #         recently_viewed.append(product.id)
# #         # Limit the number of stored products (e.g., 5)
# #         if len(recently_viewed) > 5:
# #             recently_viewed.pop(0)
# #     request.session['recently_viewed'] = recently_viewed

# #     # Calculate savings
# #     you_saved, percentage_saved = None, None
# #     if product.price and product.discounted_price:
# #         you_saved = product.price - product.discounted_price
# #         percentage_saved = (you_saved / product.price) * 100

# #     # Handle ReviewForm submission
# #     review_form = ReviewForm()
# #     if request.method == 'POST':
# #         review_form = ReviewForm(request.POST)
# #         if review_form.is_valid():
# #             # Save the form data and associate with the product
# #             review = review_form.save(commit=False)
# #             review.product = product  # Link the review to the product
# #             review.save()  # Save the review to the database
# #             messages.success(request, "Your review has been submitted successfully!")
# #             return redirect('product', slug=slug)  # Redirect to avoid form resubmission
# #         else:
# #             messages.error(request, "There was an error submitting your review. Please correct the form.")

# #     # Handle ProductQueryAskForm submission (untouched logic)
# #     form = ProductQueryAskForm(request.POST or None)
# #     if request.method == 'POST' and form.is_valid() and 'query_submit' in request.POST:
# #         form.save()
# #         messages.success(request, "Your query has been submitted successfully!")
# #         return redirect('product', slug=slug)
    
# #      # Handle Add to Cart and Buy Now actions
# #     if request.method == 'POST':
# #         action = request.POST.get('action')
# #         quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

# #         if action == 'add_to_cart':
# #             return add_to_cart(request, product, quantity)
# #         elif action == 'buy_now':
# #             return buy_now(request, product, quantity)
        

# #     cart = request.session.get('cart', {})  # Get cart from session
# #     product_quantity = cart.get(str(product.id), 1)  # Default to 1 if not in cart




# #     # Context for the template
# #     context = {
# #         'product': product,
# #         'variants': variants,
# #         'big_variants': big_variants,
# #         'you_saved': you_saved,
# #         'percentage_saved': percentage_saved,
# #         'reviews': reviews,
# #         'review_form': review_form,
# #         'form': form,
# #         'related_products':related_products,
# #         'product_quantity':product_quantity,
        
# #     }

# #     return render(request, 'app/product_page.html', context)

# def product_page(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     variants = ProductImage.objects.all()
#     big_variants = ProductBigImage.objects.all()
#     reviews = product.reviews.all()
#     related_products = Product.objects.exclude(id=product.id)[:4]

#     # Access session only for authenticated users
#     recently_viewed = request.session.get('recently_viewed', [])
#     if product.id not in recently_viewed:
#         recently_viewed.append(product.id)
#         if len(recently_viewed) > 5:
#             recently_viewed.pop(0)
#     request.session['recently_viewed'] = recently_viewed

#     # Calculate savings
#     you_saved, percentage_saved = None, None
#     if product.price and product.discounted_price:
#         you_saved = product.price - product.discounted_price
#         percentage_saved = (you_saved / product.price) * 100

#     # Handle ReviewForm submission
#     review_form = ReviewForm()
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST)
#         if review_form.is_valid():
#             review = review_form.save(commit=False)
#             review.product = product
#             review.save()
#             messages.success(request, "Your review has been submitted successfully!")
#             return redirect('product', slug=slug)
#         else:
#             messages.error(request, "There was an error submitting your review. Please correct the form.")

#     # Handle ProductQueryAskForm submission
#     form = ProductQueryAskForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid() and 'query_submit' in request.POST:
#         form.save()
#         messages.success(request, "Your query has been submitted successfully!")
#         return redirect('product', slug=slug)

#     # Handle Add to Cart and Buy Now actions
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         quantity = int(request.POST.get('quantity', 1))

#         if action == 'add_to_cart':
#             return add_to_cart(request, product, quantity)
#         elif action == 'buy_now':
#             return buy_now(request, product, quantity)

#     cart = request.session.get('cart', {})
#     product_quantity = cart.get(str(product.id), 1)

#     context = {
#         'product': product,
#         'variants': variants,
#         'big_variants': big_variants,
#         'you_saved': you_saved,
#         'percentage_saved': percentage_saved,
#         'reviews': reviews,
#         'review_form': review_form,
#         'form': form,
#         'related_products': related_products,
#         'product_quantity': product_quantity,
#     }

#     return render(request, 'app/product_page.html', context)



# @login_required
# def add_to_cart(request, product, quantity):
#     color_name = request.POST.get('option-0')
#     size_name = request.POST.get('option-1')

#     if not color_name or not size_name:
#         messages.error(request, "Please select both color and size.")
#         return redirect(request.META.get('HTTP_REFERER', '/'))

#     color = get_object_or_404(Color, name=color_name)
#     size = get_object_or_404(Size, name=size_name)

#     if request.user.is_authenticated:
#         # Use the user for authenticated users
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         # Use the session key for anonymous users
#         session_key = request.session.session_key
#         if not session_key:
#             request.session.create()  # Create a session if none exists
#             session_key = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_key=session_key)

#     # Add or update the cart item
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
#     cart_item.quantity = int(quantity)
#     cart_item.save()

#     messages.success(request, "Item added to cart!")
#     return redirect(reverse('cart'))



# @login_required
# def cart_page(request):
   
#     cart, created = Cart.objects.get_or_create(user=request.user)

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

#             # Handle quantity update
#             if quantity:
#                 quantity = int(quantity)
#                 if quantity <= 0:
#                     return JsonResponse({'success': False, 'error': 'Quantity must be greater than zero'}, status=400)

#                 cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
#                 if cart_item:
#                     cart_item.quantity = quantity
#                     cart_item.save()

#             # Calculate updated cart items, subtotal, and count
#             cart_items = cart.cartitem_set.all()
#             subtotal = sum(item.total_price for item in cart_items)
#             cart_count = cart_items.count()

#             response_data = {
#                 'success': True,
#                 'cart_count': cart_count,  # Add cart count
#                 'cart_items': [
#                     {
#                         'id': item.id,
#                         'quantity': item.quantity,
#                         'total_price': float(item.total_price),
#                         'product': {
#                             'name': item.product.name,
#                             'image_url': item.product.main_image.url if item.product.main_image else None,
#                             'price': float(item.product.price),
#                         }
#                     }
#                     for item in cart_items
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
#     subtotal = sum(item.total_price for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#     }
#     return render(request, 'app/cart.html', context)


# @login_required
# def buy_now(request, product, quantity):
#     color_name = request.POST.get('option-0')
#     size_name = request.POST.get('option-1')

#     if not color_name or not size_name:
#         messages.error(request, "Please select both color and size.")
#         return redirect(request.META.get('HTTP_REFERER', '/'))

#     color = get_object_or_404(Color, name=color_name)
#     size = get_object_or_404(Size, name=size_name)

  
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, color=color, size=size)
#     cart_item.quantity += int(quantity)
#     cart_item.save()

#     return redirect(reverse('checkout'))

# @login_required
# def checkout(request):
#     # Fetch all cart items for the current user or session
    
#     cart = Cart.objects.filter(user=request.user).first()


#     if not cart:
#         messages.error(request, "Your cart is empty.")
#         return HttpResponseRedirect('/shop/')

#     # Initialize forms
#     checkout_form = CheckoutForm()
#     payment_form = PaymentForm()

#     # Handle POST request for CheckoutForm
#     if request.method == request.POST:
#         checkout_form = CheckoutForm(request.POST)
#         if checkout_form.is_valid():
#             checkout_form.save()
#             messages.success(request, "Billing details saved successfully!")
#             return redirect("checkout")  # Redirect to refresh the page
#         else:
#             messages.error(request, "Please correct the errors in the billing form.")

#     # Handle POST request for PaymentForm
#     elif request.method ==  request.POST:
#         payment_form = PaymentForm(request.POST)
#         if payment_form.is_valid():
#             payment_form.save()
#             messages.success(request, "Payment completed successfully!")
#             return redirect("success")  # Redirect to a success page
#         else:
#             messages.error(request, "Please correct the errors in the payment form.")

#     # Calculate totals
#     cart_items = cart.cartitem_set.all()
#     subtotal = sum(item.total_price for item in cart_items)
#     shipping_cost = Decimal("50.00")  # Example shipping cost
#     total_cost = subtotal + shipping_cost

#     context = {
#         "cart_items": cart_items,
#         "checkout_form": checkout_form,
#         "payment_form": payment_form,
#         "subtotal": subtotal,
#         "shipping_cost": shipping_cost,
#         "total_cost": total_cost,
#     }
#     return render(request, "app/checkout.html", context)


# def listview(request):
#     context= {}
#     return render(request, 'app/shop_listview.html', context)



# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             # Save the new user
#             user = form.save()
#             login(request, user)  # Log the user in automatically after registration
#             return redirect('home')  # Redirect to the home page or wherever
#     else:
#         form = RegisterForm()

#     context = {'form': form}
#     return render(request, 'app/register.html', context)



# def login_page(request):
#     if request.user.is_authenticated:
#         return redirect('home')  # Redirect to home if the user is already logged in

#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # Authenticate and log the user in
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 login(request, user)  # Log the user in
#                 return redirect('home')  # Redirect to a page after successful login
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid form submission.")
#     else:
#         form = AuthenticationForm()

#     context = {
#         'form': form
#     }
#     return render(request, 'app/login.html', context)


# def logout_view(request):
#     logout(request)  # Automatically deletes the session
#     return redirect('login')



# def wishlist(request, slug):
#     product= get_object_or_404(Product, slug=slug)

#     context={'product':product }
#     return render(request, 'app/wishlist.html', context)


# def thank_you(request):
    
#     context={}

#     return render(request, 'app/thanks.html', context)


from decimal import Decimal
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from app.forms import CheckoutForm, PaymentForm, ProductQueryAskForm, RegisterForm, ReviewForm
from app.models import Brand, Cart, CartItem, Category, Color, Product, ProductBigImage, ProductImage, Size, SliderImages, Tag

# Create your views here.
def index(request, slug=None):
    slider = SliderImages.objects.all()
    
    if slug:
        # If slug is provided, filter the product by slug
        products = get_object_or_404(Product, slug=slug)
        variants = ProductImage.objects.filter(product=products)
        context = {'slider': slider, 'products': products, 'stars': range(5), 'variants': variants}
    else:
        # If no slug is provided, return all products (or a default set)
        featured_products = Product.objects.filter(is_featured=True)[:6]
        new_products = Product.objects.filter(is_new=True)[:4]

        variants = ProductImage.objects.all()  # Or adjust this to show a default set
        context = {
            'slider': slider,
            'featured_products': featured_products,
            'new_products': new_products,
            'stars': range(5),
            'variants': variants
        }
    
    return render(request, 'app/index.html', context)

def shop_page(request):
    categories = Category.objects.filter(parent__isnull=True)
    products = Product.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()
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
        'colors': colors,
        'sizes': sizes,
        'brands': brands,
        'tags': tags,
        'selected_size': selected_size,
        'sort_option': sort_option,
        'product_count': product_count,
    }
    return render(request, 'app/shop.html', context)

@login_required
def product_page(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = ProductImage.objects.all()
    big_variants = ProductBigImage.objects.all()
    reviews = product.reviews.all()
    related_products = Product.objects.exclude(id=product.id)[:4]

    # Access session only for authenticated users
    recently_viewed = request.session.get('recently_viewed', [])
    if product.id not in recently_viewed:
        recently_viewed.append(product.id)
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
            review = review_form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('product', slug=slug)
        else:
            messages.error(request, "There was an error submitting your review. Please correct the form.")

    # Handle ProductQueryAskForm submission
    form = ProductQueryAskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid() and 'query_submit' in request.POST:
        form.save()
        messages.success(request, "Your query has been submitted successfully!")
        return redirect('product', slug=slug)

    # Handle Add to Cart and Buy Now actions
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))

        if action == 'add_to_cart':
            return add_to_cart(request, product, quantity)
        elif action == 'buy_now':
            return buy_now(request, product, quantity)

    cart = request.session.get('cart', {})
    product_quantity = cart.get(str(product.id), 1)

    context = {
        'product': product,
        'variants': variants,
        'big_variants': big_variants,
        'you_saved': you_saved,
        'percentage_saved': percentage_saved,
        'reviews': reviews,
        'review_form': review_form,
        'form': form,
        'related_products': related_products,
        'product_quantity': product_quantity,
    }

    return render(request, 'app/product_page.html', context)

@login_required
def add_to_cart(request, product, quantity):
    color_name = request.POST.get('option-0')
    size_name = request.POST.get('option-1')

    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    color = get_object_or_404(Color, name=color_name)
    size = get_object_or_404(Size, name=size_name)

    # Since the view is protected, user is authenticated
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, color=color, size=size
    )
    cart_item.quantity = int(quantity)
    cart_item.save()

    messages.success(request, "Item added to cart!")
    return redirect(reverse('cart'))

@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

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

                cart_item = CartItem.objects.filter(id=item_id, cart=cart).first()
                if cart_item:
                    cart_item.quantity = quantity
                    cart_item.save()

            # Calculate updated cart items, subtotal, and count
            cart_items = cart.cartitem_set.all()
            subtotal = sum(item.total_price for item in cart_items)
            cart_count = cart_items.count()

            response_data = {
                'success': True,
                'cart_count': cart_count,  # Add cart count
                'cart_items': [
                    {
                        'id': item.id,
                        'quantity': item.quantity,
                        'total_price': float(item.total_price),
                        'product': {
                            'name': item.product.name,
                            'image_url': item.product.main_image.url if item.product.main_image else None,
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

    # Handle item removal via GET request
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
    subtotal = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }
    return render(request, 'app/cart.html', context)

@login_required
def buy_now(request, product, quantity):
    color_name = request.POST.get('option-0')
    size_name = request.POST.get('option-1')

    if not color_name or not size_name:
        messages.error(request, "Please select both color and size.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    color = get_object_or_404(Color, name=color_name)
    size = get_object_or_404(Size, name=size_name)

    # Since the view is protected, user is authenticated
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, color=color, size=size
    )
    cart_item.quantity += int(quantity)
    cart_item.save()

    return redirect(reverse('checkout'))

@login_required
def checkout(request):
    # Fetch all cart items for the current user
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        messages.error(request, "Your cart is empty.")
        return HttpResponseRedirect('/shop/')

    # Initialize forms
    checkout_form = CheckoutForm()
    payment_form = PaymentForm()

    # Handle POST request for CheckoutForm
    if request.method == 'POST' and 'checkout_submit' in request.POST:
        checkout_form = CheckoutForm(request.POST)
        if checkout_form.is_valid():
            checkout_form.save()
            messages.success(request, "Billing details saved successfully!")
            return redirect("checkout")  # Redirect to refresh the page
        else:
            messages.error(request, "Please correct the errors in the billing form.")

    # Handle POST request for PaymentForm
    elif request.method == 'POST' and 'payment_submit' in request.POST:
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
    context = {}
    return render(request, 'app/shop_listview.html', context)

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            login(request, user)  # Log the user in automatically after registration
            return redirect('home')  # Redirect to the home page or wherever
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'app/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if the user is already logged in

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and log the user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                return redirect('home')  # Redirect to a page after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'app/login.html', context)

def logout_view(request):
    logout(request)  # Automatically deletes the session
    return redirect('login')

def wishlist(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'app/wishlist.html', context)

def thank_you(request):
    context = {}
    return render(request, 'app/thanks.html', context)
