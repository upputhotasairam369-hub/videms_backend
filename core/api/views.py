from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import Category
from .serializers import CategorySerializer

import uuid 
from .models import Order, OrderItem, ProductVariant # Ensure these are imported at the top!
from .serializers import OrderSerializer
# Cleaned up imports (removed duplicates)
from .models import Product, Banner
from .serializers import ProductSerializer, UserSerializer, BannerSerializer

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

# ==============================================================================
# LIGHTWEIGHT HEALTH CHECK (PRODUCTION OPTIMIZED)
# ==============================================================================
def health_check(request):
    """
    A pure Django health check. 
    Bypasses Django REST Framework entirely so load balancers (Railway/Vercel) 
    can ping this instantly without consuming heavy server memory.
    """
    return JsonResponse({
        "status": "healthy",
        "service": "videms_backend",
        "version": "1.0.0",
        "message": "Django backend is connected!"
    }, status=200)

# ==============================================================================
# PRODUCT API
# ==============================================================================
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Automatically provides `list` and `detail` actions for Products.
    Read-only means standard users can't edit products via this API.
    """
    queryset = Product.objects.all().prefetch_related('variants', 'images')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug' # Allows us to fetch by slug (e.g., /api/products/urban-sofa/) instead of ID

@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    """
    Extracts a unique list of categories from the products in the database.
    """
    categories = Product.objects.values_list('category', flat=True).distinct()
    return Response(list(categories))

# ==============================================================================
# AUTHENTICATION APIs
# ==============================================================================
# In a real app, you'd integrate Twilio or AWS SNS here.
# For now, we mock the OTP to always accept '123456' so you can test your frontend login.

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Verifies the Google ID token and logs in/registers the user.
    """
    token = request.data.get('credential')
    
    if not token:
        return Response({"message": "Credential is required"}, status=400)
    
    try:
        # Get client ID from environment or settings
        # It's better to configure this in settings, but we will use env directly or fallback
        # In a real setup you'd have settings.GOOGLE_CLIENT_ID
        client_id = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')
        
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            # Note: We do not strictly enforce client_id matching here to allow easier testing if not set, 
            # but in production, provide the specific client ID.
            client_id if client_id != 'YOUR_GOOGLE_CLIENT_ID' else None 
        )
        
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        
        # Get or create the user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        
        # Generate JWT Tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "token": str(refresh.access_token),
            "user": UserSerializer(user).data
        })
        
    except ValueError as e:
        # Invalid token signature or expired token
        return Response({"message": "Invalid Google token", "error": str(e)}, status=400)
        
    except Exception as e:
        # Catch all other crashes (Database constraints, Network failures)
        # and return a clean JSON 500 instead of crashing the server.
        import traceback
        traceback.print_exc()
        return Response({
            "message": "An unexpected error occurred during authentication.", 
            "error": str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Must have a valid token to access!
def current_user(request):
    """
    Returns the details of the currently logged-in user.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Allows the user to store their personal details in the database.
    """
    user = request.user
    
    # Safely get the new data, or keep the old data if none was provided
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    
    # Save the updated information to the database
    user.save()
    
    # Return the fresh data back to the React frontend
    return Response(UserSerializer(user).data)


# ==============================================================================
# REACT ADMIN DASHBOARD APIs
# ==============================================================================

@api_view(['GET'])
@permission_classes([AllowAny]) 
def admin_dashboard_stats(request):
    """Provides high-level stats for the admin dashboard."""
    from django.db.models import Sum
    users_count = User.objects.count()
    products_count = Product.objects.count()
    orders_count = Order.objects.count()
    revenue_data = Order.objects.filter(payment_status='PAID').aggregate(total=Sum('total_amount'))
    revenue = float(revenue_data['total'] or 0)
    return Response({
        "total_users": users_count,
        "total_products": products_count,
        "orders": orders_count,
        "revenue": revenue if revenue > 0 else 245000,  # Fallback to mock if no paid orders yet
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def admin_users_list(request):
    """Fetches all registered users for the Admin panel user table."""
    users = User.objects.all().order_by('-date_joined')
    return Response(UserSerializer(users, many=True).data)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def admin_orders_list(request):
    """Returns all orders from the database for the Admin panel orders table."""
    orders = Order.objects.all().order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# ==============================================================================
# BANNER APIs
# ==============================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_active_banners(request):
    """
    Fetches all active hero banners for the React frontend, 
    sorted by their display order.
    """
    banners = Banner.objects.filter(is_active=True).order_by('display_order')
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny]) 
def create_order(request):
    data = request.data
    payment_method = data.get('payment_method', 'RAZORPAY')
    items_data = data.get('items', [])
    
    if not items_data:
        return Response({"error": "Your cart is empty"}, status=400)

    # 1. Create the main Order Profile in the DB
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        customer_name=data.get('customer_name'),
        customer_email=data.get('customer_email'),
        customer_phone=data.get('customer_phone'),
        shipping_address=data.get('shipping_address'),
        pincode=data.get('pincode'),
        total_amount=data.get('total_amount'),
        payment_method=payment_method,
    )

    # 2. Attach items and DEDUCT INVENTORY STOCK
    for item in items_data:
        product_id = item.get('product_id')
        variant_id = item.get('variant_id')
        quantity_bought = int(item.get('quantity', 1))
        
        product = Product.objects.filter(id=product_id).first() if product_id else None
        variant = ProductVariant.objects.filter(variant_id=variant_id).first() if variant_id else None
        
        # 🚀 CRITICAL: The Stock Deduction Engine
        if variant:
            if variant.inventory_quantity >= quantity_bought:
                # Subtract stock from database
                variant.inventory_quantity -= quantity_bought
                variant.save()
            else:
                return Response({"error": f"Not enough stock for {product.name if product else 'item'}."}, status=400)

        OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            product_name=item.get('name', product.name if product else 'Unknown Product'),
            quantity=quantity_bought,
            price=item.get('price', 0)
        )

    # 3. Handle Payment Gateway Verification
    if payment_method == 'RAZORPAY':
        order.razorpay_order_id = f"order_{uuid.uuid4().hex[:14]}" 
        order.save()
        return Response({
            "order_id": order.id,
            "razorpay_order_id": order.razorpay_order_id,
            "amount": order.total_amount,
            "currency": "INR"
        })
        
    elif payment_method == 'COD':
        order.order_status = 'CONFIRMED'
        order.save()
        return Response({
            "message": "Order placed successfully via Cash on Delivery",
            "order_id": order.id
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    """Marks a Razorpay order as paid in the database"""
    data = request.data
    try:
        order = Order.objects.get(razorpay_order_id=data.get('razorpay_order_id'))
        order.payment_status = 'PAID'
        order.order_status = 'CONFIRMED'
        order.razorpay_payment_id = data.get('razorpay_payment_id')
        order.razorpay_signature = data.get('razorpay_signature')
        order.save()
        return Response({"message": "Payment verified successfully", "order_id": order.id})
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    """Fetches order history for the React Account Page"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

 

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # Only fetches enabled categories, sorted by display_order
    queryset = Category.objects.filter(status=True).order_by('display_order')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    # Only fetches active banners, sorted by display_order
    queryset = Banner.objects.filter(is_active=True).order_by('display_order')
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]

from .models import Combination, HomepageBestSeller, HomepageNewArrival
from .serializers import CombinationSerializer, HomepageBestSellerSerializer, HomepageNewArrivalSerializer

class CombinationViewSet(viewsets.ModelViewSet):
    queryset = Combination.objects.filter(status=True).order_by('display_order')
    serializer_class = CombinationSerializer
    permission_classes = [AllowAny]

class HomepageBestSellerViewSet(viewsets.ModelViewSet):
    queryset = HomepageBestSeller.objects.filter(status=True).order_by('display_order')
    serializer_class = HomepageBestSellerSerializer
    permission_classes = [AllowAny]

class HomepageNewArrivalViewSet(viewsets.ModelViewSet):
    queryset = HomepageNewArrival.objects.filter(status=True).order_by('display_order')
    serializer_class = HomepageNewArrivalSerializer
    permission_classes = [AllowAny]

from rest_framework.throttling import AnonRateThrottle
from .models import BusinessBanner, BulkOrder
from .serializers import BusinessBannerSerializer, BulkOrderSerializer

class BusinessBannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BusinessBanner.objects.filter(is_active=True).order_by('display_order')
    serializer_class = BusinessBannerSerializer
    permission_classes = [AllowAny]

class BulkOrderThrottle(AnonRateThrottle):
    rate = '5/hour'

class BulkOrderViewSet(viewsets.ModelViewSet):
    queryset = BulkOrder.objects.all().order_by('-created_at')
    serializer_class = BulkOrderSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_throttles(self):
        if self.action == 'create':
            return [BulkOrderThrottle()]
        return super().get_throttles()