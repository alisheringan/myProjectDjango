from pathlib import Path
import os
import os
import certifi

# Использовать сертификаты certifi для SSL
os.environ['SSL_CERT_FILE'] = certifi.where()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-5uo2tc_vkbi_b+ebny!ep0cb(hlgjr!(t9%=5vi7hp=!3a0(oq"

DEBUG = True

ALLOWED_HOSTS = []


# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
]


# -----------------------------
# MIDDLEWARE
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------
# URL / WSGI
# -----------------------------
ROOT_URLCONF = "myproject.urls"

WSGI_APPLICATION = "myproject.wsgi.application"


# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -----------------------------
# LOCALIZATION
# -----------------------------
TIME_ZONE = 'Asia/Bishkek'
USE_TZ = True

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]

USE_I18N = True
USE_L10N = True

LANGUAGE_COOKIE_NAME = "django_language"

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'blog/static'),
]

# Для Heroku/деплоя/проекта можно использовать STATIC_ROOT
if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# -----------------------------
# MEDIA FILES
# -----------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# -----------------------------
# EMAIL SETTINGS
# -----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'momunaliev.alisher@gmail.com'

# Для реальной отправки:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'momunaliev.alisher@gmail.com'
# EMAIL_HOST_PASSWORD = 'password'


# -----------------------------
# LOGIN/LOGOUT
# -----------------------------
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = '/'


# -----------------------------
# CACHING
# -----------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
    }
}


# -----------------------------
# DEFAULT FIELD TYPE
# -----------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'momunaliev.alisher@gmail.com'   # Твой email
EMAIL_HOST_PASSWORD = 'mirzrmqdvgikdoja'  # Для Gmail нужен App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



DEBUG = False
ALLOWED_HOSTS = ["*"]
STATIC_ROOT = BASE_DIR / "staticfiles"

