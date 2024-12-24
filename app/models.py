from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify


# Create your models here.

class Tag(models.Model):
    name= models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    slug= models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug= slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductQueryAsk(models.Model):  # Fixed typo in class name
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=150)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)  
    message= models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name
    


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Red", "Black"
    code = models.CharField(max_length=7, unique=True)  # e.g., "#FF0000"

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)  # e.g., "XS", "S", "M", "L", "XL"

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug= models.SlugField(unique=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    SKU = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField()
    rating = models.FloatField()
    reviews_count = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    available_colors = models.ManyToManyField(Color, blank=True)
    available_sizes = models.ManyToManyField(Size, blank=True)
    product_type = models.CharField(max_length=50)
    collection = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='app/images/product_images/')
    hover_image = models.ImageField(upload_to='app/images/product_images/', blank=True, null=True)
    discount_percentage = models.IntegerField(null=True, blank=True)
    limited_stock_message = models.CharField(max_length=255, null=True, blank=True)
    is_featured= models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    def __str__(self):
        return self.name


    def add_to_cart_url(self):
        # Generates a URL for adding this product to the cart
        return reverse('add_to_cart', kwargs={'product_id': self.id})
    
    def buy_now_url(self):
        # Generates a URL for the Buy It Now functionality
        return reverse('buy_now', kwargs={'product_id': self.id})
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    

class ProductBigImage(models.Model):
    product = models.ForeignKey(Product, related_name='big_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_big_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Open the image to get dimensions
        if self.image:
            img = Image.open(self.image)
            self.width, self.height = img.size
        super().save(*args, **kwargs)  # Call the "real" save method

    def __str__(self):
        return f"Big Image for {self.product.name}"
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class SliderImages(models.Model):
    title= models.CharField(max_length=200)
    subtitle= models.CharField(max_length=400, blank=True)
    image= models.ImageField()

    def __str__(self):
        return self.title
    
# Models (for cart and order)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True, default='')
    terms_agreed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart (User: {self.user}, Session: {self.session_key})"
    
    def add_item(self, product, quantity):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        cart_item.quantity += quantity
        cart_item.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='pending')
    # Additional fields like payment status, shipping details, etc.


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100) 
    email = models.EmailField()  
    rating = models.PositiveIntegerField()  
    review_title = models.CharField(max_length=200, blank=True, null=True)  
    comment = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.rating} stars)"
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    

class Checkout(models.Model):
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100, null=True, blank=True)
    email= models.EmailField(max_length=100)
    telephone= PhoneNumberField(null=False, unique=True)
    company= models.CharField(max_length=100, null=True, blank=True)
    address= models.CharField(max_length=500)
    apartment= models.CharField(max_length=50, blank=True, null=True)
    city= models.CharField(max_length=200)
    post_code= models.IntegerField(null=True, blank=True)
    country= models.CharField(max_length=200)
    state= models.CharField(max_length=200, null=True, blank=True)
    order_notes= models.TextField(null=True, blank=True)



class Payment(models.Model):
    CARD_TYPES = [
        (1, "American Express"),
        (2, "Visa Card"),
        (3, "Master Card"),
        (4, "Discover Card"),
    ]

    cardname = models.CharField(max_length=100)
    cardtype = models.PositiveSmallIntegerField(choices=CARD_TYPES)
    cardno = models.CharField(max_length=16)  # Use CharField for card number
    cvv = models.CharField(max_length=3)  # CVV is typically 3 or 4 digits
    exdate = models.DateField()  # Expiration date