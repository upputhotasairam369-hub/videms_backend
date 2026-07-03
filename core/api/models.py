from django.db import models

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