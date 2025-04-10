import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = ['https://admission.imcbs.com'
    ,
    
]
# Security settings
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "admission.imcbs.com", "www.admission.imcbs.com"]




# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admitionapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admitionapp.middleware.NoCacheMiddleware', 
]

ROOT_URLCONF = 'admitionproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'admitionproject.wsgi.application'

# Database settings
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv("DB_NAME", "admitionproject"),
#         'USER': os.getenv("DB_USER", "postgres"),
#         'PASSWORD': os.getenv("DB_PASSWORD", "1234"),
#         'HOST': os.getenv("DB_HOST", "localhost"),
#         'PORT': os.getenv("DB_PORT", "5432"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'admission',  # Replace with your database name
        'USER': 'postgres',  # Replace with your database username
        'PASSWORD': 'info@imc',  # Replace with your database password
        'HOST': 'localhost',  # Use 'localhost' for local development
        'PORT': '5432',  # Default PostgreSQL port
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


import os

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
LOGIN_URL = '/admin-login/'  # Change to your actual login URL

# Ensure this folder exists
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Ensure BASE_DIR is properly set
]

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'  # Helps with cross-domain requests
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3600 * 24 * 7  # 1 week in seconds
SESSION_SAVE_EVERY_REQUEST = True  # Helps keep session alive