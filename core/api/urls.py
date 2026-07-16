# videms_backend/core/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CategoryViewSet, BannerViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'combinations', views.CombinationViewSet, basename='combination')
router.register(r'home/bestsellers', views.HomepageBestSellerViewSet, basename='home-bestseller')
router.register(r'home/new-arrivals', views.HomepageNewArrivalViewSet, basename='home-new-arrival')
router.register(r'business-banner', views.BusinessBannerViewSet, basename='business-banner')
router.register(r'bulk-orders', views.BulkOrderViewSet, basename='bulk-order')
urlpatterns = [
    path('health/', views.health_check, name='health-check'), 
    path('', include(router.urls)),
    
    path('auth/google/', views.google_login, name='google-login'),
    path('auth/me/', views.current_user, name='current-user'),
    path('auth/me/update/', views.update_profile, name='update-profile'),
    
    # 🚀 Add these 3 new React Admin Panel Routes:
    path('admin-api/dashboard/', views.admin_dashboard_stats, name='admin-dashboard'),
    path('admin-api/users/', views.admin_users_list, name='admin-users'),
    path('admin-api/orders/', views.admin_orders_list, name='admin-orders'),

    ### Order details ##
    path('orders/create/', views.create_order, name='create-order'),
    path('orders/verify/', views.verify_payment, name='verify-payment'),
    path('orders/my-orders/', views.my_orders, name='my-orders') , 

]
