import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------
# SECURITY CONFIG
# ---------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

# ---------------------------
# INSTALLED APPS
# ---------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local apps
    'documents',
]

# ---------------------------
# MIDDLEWARE
# ---------------------------
MIDDLEWARE = [
    # CORS must be FIRST
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------
# URL / WSGI
# ---------------------------
ROOT_URLCONF = 'knowledgebase.urls'
WSGI_APPLICATION = 'knowledgebase.wsgi.application'

# ---------------------------
# TEMPLATES
# ---------------------------
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

# ---------------------------
# CORS CONFIG
# ---------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ["*"]

# ---------------------------
# DATABASE (SQLite)
# ---------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------
# PASSWORD VALIDATION
# ---------------------------
AUTH_PASSWORD_VALIDATORS = []

# ---------------------------
# INTERNATIONALIZATION
# ---------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------
# STATIC + MEDIA
# ---------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   # needed for Render

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media folder exists
os.makedirs(MEDIA_ROOT, exist_ok=True)
