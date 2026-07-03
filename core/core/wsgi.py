# core/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# Points the server to your specific settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Exposes the application callable for the server to use
application = get_wsgi_application()