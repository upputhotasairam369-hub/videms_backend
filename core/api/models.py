from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """
    The core product table. Holds universal details about the item.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="URL friendly name (e.g., urban-ladder-sofa)")
    brand = models.CharField(max_length=100)
    
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    
    # 🚀 ADDED: The description field for the Admin Panel
    description = models.TextField(blank=True, null=True, help_text="Detailed product description")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    """
    Holds pricing and inventory. Connected to Product via a Foreign Key.
    If a sofa has different sizes or colors, each gets a variant.
    """
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    variant_id = models.CharField(max_length=100, unique=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Selling price")
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Original MRP", null=True, blank=True)
    
    inventory_quantity = models.IntegerField(default=0, help_text="Total stock available")
    inventory_reserved = models.IntegerField(default=0, help_text="Stock currently in someone's cart")

    def __str__(self):
        return f"{self.product.name} - {self.variant_id}"

    @property
    def discount_percentage(self):
        """Calculates the 19% OFF badge seen on your frontend dynamically."""
        if self.compare_price and self.compare_price > self.price:
            discount = ((self.compare_price - self.price) / self.compare_price) * 100
            return round(discount)
        return 0

class ProductImage(models.Model):
    """
    Holds the image files. Connected to Product via a Foreign Key.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/') 
    is_primary = models.BooleanField(default=False, help_text="Is this the main thumbnail?")

    def __str__(self):
        return f"Image for {self.product.name}"

class Banner(models.Model):
    title = models.CharField(max_length=200, help_text="Main headline for the banner (e.g., 'Summer Sale')")
    subtitle = models.TextField(blank=True, null=True, help_text="Sub-text under the headline")
    tag = models.CharField(max_length=50, blank=True, null=True, default="Featured", help_text="Small tag like 'New Arrival'")
    
    image = models.ImageField(upload_to='banners/', help_text="Upload the banner image from your computer")
    
    link_url = models.CharField(max_length=500, default='/products', help_text="Where should this banner take the user?")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this banner from the website")
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first (e.g., 1 comes before 5)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Hero Banner'
        verbose_name_plural = 'Hero Banners'

    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Hidden'})"

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('RAZORPAY', 'Razorpay'),
        ('COD', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    # Link the order to a registered user (nullable for guest checkouts)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Customer Details
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    # Order Totals
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Statuses
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='RAZORPAY')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    
    # Razorpay Specifics
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True) 
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Store a snapshot of the name and price so it doesn't change on past receipts if you update the product later
    product_name = models.CharField(max_length=255) 
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price at the time of purchase")

    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Order #{self.order.id})" 

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to='categories/images/')
    display_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Combination(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Living Room Collection")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='combinations/images/')
    products = models.ManyToManyField(Product, related_name='combinations', blank=True)
    display_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True, help_text="Enable/Disable combination")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title

class HomepageBestSeller(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    display_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True, help_text="Enable/Disable on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"Bestseller: {self.product.name}"

class HomepageNewArrival(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    display_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True, help_text="Enable/Disable on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"New Arrival: {self.product.name}"