# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, ProductImage, ProductVariant
from .models import Product, Banner
from .models import Order, OrderItem, Category  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProductImageSerializer(serializers.ModelSerializer):
    # We want the absolute URL to serve to the React <img src={} /> tags
    url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['url', 'is_primary']

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            url = request.build_absolute_uri(obj.image.url)
            # Force HTTPS — Railway terminates SSL at the proxy, so Django sees HTTP
            return url.replace('http://', 'https://')
        return None

class ProductVariantSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.ReadOnlyField()
    class Meta:
        model = ProductVariant
        fields = ['variant_id', 'price', 'compare_price', 'inventory_quantity', 'inventory_reserved', 'discount_percentage']

class ProductSerializer(serializers.ModelSerializer):
    # This nests the images and variants inside the main Product JSON object!
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product 
         # 🚀 ADD 'description' TO THIS LIST
        fields = [
            'id', 'name', 'slug', 'brand', 'category', 'subcategory', 
            'item_type', 'finish', 'description', 'images', 'variants'
        ]


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'tag', 'image', 'link_url', 'display_order']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

# Order details #######
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'variant', 'product_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # Nests the purchased items inside the main order JSON
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_email', 'customer_phone', 
            'shipping_address', 'pincode', 'total_amount', 
            'payment_method', 'payment_status', 'order_status', 
            'razorpay_order_id', 'created_at', 'items'
        ]


##### Categories Serializers ######### 

class CategorySerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'cover_image', 'display_order', 'status']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

from .models import Combination, HomepageBestSeller, HomepageNewArrival

class CombinationSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Combination
        fields = ['id', 'title', 'slug', 'description', 'cover_image', 'products', 'display_order', 'status']

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

class HomepageBestSellerSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = HomepageBestSeller
        fields = ['id', 'product', 'display_order', 'status']

class HomepageNewArrivalSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = HomepageNewArrival
        fields = ['id', 'product', 'display_order', 'status']
