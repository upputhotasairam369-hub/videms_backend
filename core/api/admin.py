# api/admin.py
from django.contrib import admin
from .models import Product, ProductVariant, ProductImage
from .models import Product, Banner # Make sure to import Banner!

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Provides 1 empty row to add a new variant/price easily

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Provides 1 empty row to upload a new image

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Displays these columns in the main product list
    list_display = ('name', 'brand', 'category', 'subcategory')
    
    # Adds a filter sidebar
    list_filter = ('category', 'brand')
    
    # Adds a search bar
    search_fields = ('name', 'brand')
    
    # Automatically fills out the slug field as the superuser types the product name
    prepopulated_fields = {'slug': ('name',)}
    
    # Attaches the Variants and Images to the bottom of the Product entry page
    inlines = [ProductVariantInline, ProductImageInline]


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'is_active', 'display_order', 'created_at')
    list_editable = ('is_active', 'display_order') # Allows you to turn banners on/off quickly
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'tag')