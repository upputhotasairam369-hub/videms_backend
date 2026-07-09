# videms_backend/core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.view import home_view # Keeping your custom home view!

urlpatterns = [
    # The built-in Django Admin panel
    path('admin/', admin.site.urls),
    
    # Your custom testing view
    path('', home_view, name='home'),

    # Route all API requests to our 'api' application's urls.py file
    # Ensure this matches your folder structure! If 'api' is inside 'core', change to 'core.api.urls'
    path('api/', include('api.urls')), 
]

# --- SERVE MEDIA FILES ---
# Serves uploaded images (products, banners) in both development and production.
# In production on Railway, WhiteNoise handles static files but not media,
# so Django must serve media files directly.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)