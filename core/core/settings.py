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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'storages',

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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
        # Replace 'postgres:postgres' with your local postgres username and password.
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Enable WhiteNoise to compress and serve static files
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# AWS S3 Configuration for Media Files
# Using the variables from the user's snippet
AWS_ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKET')
AWS_S3_REGION_NAME = os.environ.get('REGION')
AWS_S3_ENDPOINT_URL = os.environ.get('ENDPOINT')

if AWS_ACCESS_KEY_ID and AWS_STORAGE_BUCKET_NAME:
    # Use S3 for media storage if AWS variables are set
    STORAGES["default"]["BACKEND"] = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
WHITENOISE_MANIFEST_STRICT = False

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# 5. CORS & CSRF (REACT INTEGRATION)
# ==============================================================================
# CORS_ALLOWED_ORIGINS must be a LIST of strings, never True/False.
# CORS_ALLOW_ALL_ORIGINS=True + CORS_ALLOW_CREDENTIALS=True is also invalid in browsers.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://videmsfronted.vercel.app",
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://videmsbackend-production.up.railway.app",
    "https://videmsfronted.vercel.app",
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
    'BLACKLIST_AFTER_ROTATION': False,  # token_blacklist not in INSTALLED_APPS — must be False
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}