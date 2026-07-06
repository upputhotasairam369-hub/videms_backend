from pathlib import Path
from datetime import timedelta
import os
# pyrefly: ignore [missing-import]
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# 1. SECURITY & ENVIRONMENT
# ==============================================================================
# In production, Railway will inject the SECRET_KEY environment variable.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-your-super-secret-key-goes-here')

# True locally, False in Railway production
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Allow Railway to host the application
ALLOWED_HOSTS = ['*', 'videmsbackend-production.up.railway.app', 'localhost', '127.0.0.1']

# ==============================================================================
# 2. APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # --- Third-Party Apps ---
    'rest_framework',         
    'rest_framework_simplejwt', 
    'corsheaders',            

    # --- Local Apps ---
    'api'                
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # MUST be at the top
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Helps serve static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ==============================================================================
# 3. DATABASE CONFIGURATION
# ==============================================================================
# Automatically switches: Uses Railway's DATABASE_URL in production, 
# and falls back to your local PostgreSQL when developing on your machine.
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:EAspUlLarAmEHGpplTLdMjSEcSDNcLDk@postgres.railway.internal:5432/railway',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# 4. STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Required for production

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# 5. CORS & CSRF (REACT INTEGRATION)
# ==============================================================================
FRONTEND_URLS = os.environ.get("FRONTEND_URLS", "http://localhost:3000")
CORS_ALLOWED_ORIGINS = FRONTEND_URLS.split(",")
CSRF_TRUSTED_ORIGINS = FRONTEND_URLS.split(",") + [
    "https://videmsbackend-production.up.railway.app"
]

# ==============================================================================
# 6. DJANGO REST FRAMEWORK & JWT
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}