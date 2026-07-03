# api/apps.py
from django.apps import AppConfig

class ApiConfig(AppConfig):
    # Uses a 64-bit integer for primary keys (IDs). This is the modern standard
    # to ensure you never run out of IDs as your store grows.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'