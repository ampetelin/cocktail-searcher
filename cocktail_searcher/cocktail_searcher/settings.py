import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variable
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_spectacular',
    'apps.cocktails',
    'apps.telegram',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'utils.rest_framework.pagination.CustomPageNumberPagination',
    'DEFAULT_SCHEMA_CLASS': 'utils.drf_spectacular.openapi.CustomAutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Cocktail Searcher API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cocktail_searcher.urls'

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

WSGI_APPLICATION = 'cocktail_searcher.wsgi.application'

# SECURITY WARNING: proxy should set a header to indicate secure connections
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

LOGGING_LEVEL = env('LOGGING_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{process}] [{levelname}] [{name}] - {message}',
            'style': '{',
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'root': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
        },
        'django': {
            'level': 'INFO',
            'handlers': ['django'],
            'propagate': False,
        },
        'django.server': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sentry
sentry_sdk.init(
    dsn=env('SENTRY_DSN', default=None),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)

# Inshaker Parser
INSHAKER_BASE_URL = env('INSHAKER_BASE_URL', default='https://ru.inshaker.com')
INSHAKER_COCKTAILS_PATH = env('INSHAKER_COCKTAILS_PATH', default='/cocktails')
INSHAKER_COCKTAIL_URLS_XPATH = env('INSHAKER_COCKTAIL_URLS_XPATH', default='//a[@class="cocktail-item-preview"]/@href')
INSHAKER_COCKTAIL_NAME_XPATH = env('INSHAKER_COCKTAIL_NAME_XPATH', default='//h1[@class="common-name"]/text()')
INSHAKER_COCKTAIL_IMAGE_XPATH = env('INSHAKER_COCKTAIL_IMAGE_XPATH', default='//img[@class="image"]/@src')
INSHAKER_COCKTAIL_CATEGORIES_XPATH = env('INSHAKER_COCKTAIL_CATEGORIES_XPATH',
                                         default='//ul[@class="tags"]/li/a/text()')
INSHAKER_COCKTAIL_INGREDIENTS_XPATH = env('INSHAKER_COCKTAIL_INGREDIENTS_XPATH',
                                          default='//div[@class="ingredient-tables"]/table[1]/tr[position()>1]')
INSHAKER_INGREDIENT_NAME_XPATH = env('INSHAKER_INGREDIENT_NAME_XPATH', default='td[@class="name"]/a/text()')
INSHAKER_INGREDIENT_AMOUNT_XPATH = env('INSHAKER_INGREDIENT_AMOUNT_XPATH', default='td[@class="amount"]/text()')
INSHAKER_INGREDIENT_UNIT_XPATH = env('INSHAKER_INGREDIENT_UNIT_XPATH', default='td[@class="unit"]/text()')
INSHAKER_COCKTAIL_RECIPE_XPATH = env('INSHAKER_COCKTAIL_RECIPE_XPATH',
                                     default='//ul[@itemprop="recipeInstructions"]/li/text()')
