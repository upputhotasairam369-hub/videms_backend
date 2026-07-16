# api/admin.py
from django.contrib import admin
from .models import Product, ProductVariant, ProductImage, Banner, Order, OrderItem 
from .models import Category, Subcategory

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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Prevents empty blank rows from showing up
    readonly_fields = ('product_name', 'price', 'quantity') # Prevents accidental editing of past receipts

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount', 'payment_method', 'payment_status', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email', 'razorpay_order_id', 'id')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'total_amount')
    
    # This attaches the purchased items directly inside the Order view
    inlines = [OrderItemInline] 
    
    # Allows you to quickly change the order status from the main table view
    list_editable = ('order_status',) 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'status', 'created_at')
    list_editable = ('display_order', 'status')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'display_order', 'status', 'created_at')
    list_editable = ('display_order', 'status')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'status')
    search_fields = ('name', 'category__name')

from .models import Combination, HomepageBestSeller, HomepageNewArrival

@admin.register(Combination)
class CombinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_order', 'status', 'created_at')
    list_editable = ('display_order', 'status')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('products',)
    search_fields = ('title',)

@admin.register(HomepageBestSeller)
class HomepageBestSellerAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_order', 'status', 'created_at')
    list_editable = ('display_order', 'status')
    search_fields = ('product__name',)

@admin.register(HomepageNewArrival)
class HomepageNewArrivalAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_order', 'status', 'created_at')
    list_editable = ('display_order', 'status')
    search_fields = ('product__name',)

import csv
from django.http import HttpResponse
from .models import BusinessBanner, BulkOrder

@admin.action(description='Export Selected to CSV')
def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)

    return response

@admin.register(BusinessBanner)
class BusinessBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'small_heading', 'display_order', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title', 'subtitle', 'small_heading')
    list_filter = ('is_active',)

@admin.register(BulkOrder)
class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'customer_name', 'email', 'business_type', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'business_type', 'created_at')
    search_fields = ('company_name', 'customer_name', 'email', 'phone')
    actions = [export_as_csv]