from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 

# Cleaned up imports (removed duplicates)
from .models import Product, Banner
from .serializers import ProductSerializer, UserSerializer, BannerSerializer

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
def send_otp(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({"message": "Phone number is required"}, status=400)
    
    # MOCK: In production, send SMS here.
    print(f"DEBUG: Pretend we sent OTP 123456 to {phone}")
    return Response({"message": "OTP sent successfully"})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    # MOCK VERIFICATION
    if otp == '123456':
        # Create a user if they don't exist, using their phone as the username
        user, created = User.objects.get_or_create(username=phone)
        
        # Generate JWT Tokens (This is what your localStorage saves!)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "token": str(refresh.access_token),
            "user": UserSerializer(user).data
        })
    else:
        return Response({"message": "Invalid OTP"}, status=400)

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
    users_count = User.objects.count()
    products_count = Product.objects.count()
    return Response({
        "total_users": users_count,
        "total_products": products_count,
        "revenue": 245000, # Mocked metric
        "orders": 12       # Mocked metric
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
    """Mocks an empty orders list so the React frontend doesn't crash."""
    return Response([])

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