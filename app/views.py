from django.shortcuts import render

# Create your views here.
def index(request):
    context= {}
    return render(request, 'app/index.html', context)

def shop_page(request):
    context= {}
    return render(request, 'app/shop.html', context)

def product_page(request):
    context= {}
    return render(request, 'app/product_page.html', context)

def cart_page(request):
    context= {}
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
