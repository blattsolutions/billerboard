import os
import sentry_sdk
"""
Django settings for stb_billerboard project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-wi)h07)k36oewzo@_fmqc*^_t+x9^v!+(t5bly-^8@cf2tcvmb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['https://laughing-computing-machine-q6pj9q5q9qr2xjpg-8000.preview.app.github.dev', 'localhost', '127.0.0.1', 'stoneberg.work']

CSRF_TRUSTED_ORIGINS = ['https://laughing-computing-machine-q6pj9q5q9qr2xjpg-8000.preview.app.github.dev', 'http://stoneberg.work', 'https://stoneberg.work']
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_celery_results',
    'django_celery_beat',

    'allauth_ui',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.microsoft',
    'userauth',
    'avatar',
    'billerboard',
    'dataentry',
    'django_htmx',
    'widget_tweaks',
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "allauth.account.middleware.AccountMiddleware",
        "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "stb_billerboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "stb_billerboard.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    #"default": {
    #    "ENGINE": "django.db.backends.sqlite3",
    #    "NAME": BASE_DIR / "db.sqlite3",
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'billerboard',
        'USER': 'billerboard_user',
        'PASSWORD': 'Plw18*n88',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SITE_ID = 1
#ACCOUNT_DEFAULT_HTTP_PROTOCOL ='https'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Specify the context processors as follows:


AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "microsoft": {
        "APPS": [
            {
                "client_id": "ffbd855b-73de-4a72-b07b-3b03291a5174",
                "secret": "BcC8Q~VivSupQ9eUZ1NMPKC2qPaF0hu4OLpzKcxX",
                "settings": {
                    "tenant": "organizations",
                }
            }
        ]
    }
}

LOGIN_REDIRECT_URL = "login/"

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i'
TIME_FORMAT = 'H:i'
SHORT_DATE_FORMAT = 'd.m.Y'
SHORT_DATETIME_FORMAT = 'd.m.Y H:i'


#CELERY STUFF
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TIMEZONE = 'Europe/Berlin'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_IMPORTS = [
    'dataentry.tasks',
]


#watchmedo auto-restart -d stb_billerboard/ -p '*.py' -- celery -A stb_billerboard worker --concurrency=10 --beat --loglevel=info


#REDIS Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}
#CACHES = {
#    "default": {
#         "BACKEND": "django.core.cache.backends.dummy.DummyCache",
      #  "BACKEND": "django_redis.cache.RedisCache",
      #  "LOCATION": "redis://default:YY9eCOQ8YPiWADNmJy8XWXQSLZJ0dJ8F@redis-14521.c292.ap-southeast-1-1.ec2.cloud.redislabs.com:14521/0",
      #  "OPTIONS": {
      #      "CLIENT_CLASS": "django_redis.client.DefaultClient",
      #  }
#    }
#}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

#Sentry
sentry_sdk.init(
    dsn="https://7c027c8d6f7561e25c7aa47ab9217396@o4506386918342656.ingest.sentry.io/4506386920439808",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
ACCOUNT_EMAIL_VERIFICATION = 'none'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'stoneberg.work'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'no-reply@stoneberg.work' #sender's email-id
EMAIL_HOST_PASSWORD = 'Drag0nball900!' #password associated with above email-id
