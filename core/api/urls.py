# videms_backend/core/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('', include(router.urls)),
    path('categories/', views.get_categories, name='categories'),
    
    path('auth/send-otp/', views.send_otp, name='send-otp'),
    path('auth/verify-otp/', views.verify_otp, name='verify-otp'),
    path('auth/me/', views.current_user, name='current-user'),
    path('auth/me/update/', views.update_profile, name='update-profile'),
    
    # 🚀 Add these 3 new React Admin Panel Routes:
    path('admin-api/dashboard/', views.admin_dashboard_stats, name='admin-dashboard'),
    path('admin-api/users/', views.admin_users_list, name='admin-users'),
    path('admin-api/orders/', views.admin_orders_list, name='admin-orders'),
    path('banners/', views.get_active_banners, name='active-banners'),
]
