"""
Django settings for ywbweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../templates'),
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vkfmcxmke1_+ves+cxluom@4b$0sd-pl%05z(&la$_hchymui1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'merchant',
    'registration',
    'weixin',
    'django.contrib.gis',
    'surrounding',
    'offline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ywbweb.urls'

WSGI_APPLICATION = 'ywbweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.contrib.gis.db.backends.postgis',
        'NAME': 'ywbwebdb',
        'USER': 'wjbb',
        'PASSWORD': 'wjbb111',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'wjbbserverdb': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'wjbbserverdb',
        'USER': 'wjbb',
        'PASSWORD': 'wjbb111',
        'HOST': 'localhost',
        'PORT': '5432',
    },
#     'geodb': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'geodb',
#         'USER': 'wjbb',
#         'PASSWORD': 'wjbb111',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     },
#     'weixindb': {
#         'ENGINE':'django.db.backends.postgresql_psycopg2',
#         'NAME': 'weixindb',
#         'USER': 'wjbb',
#         'PASSWORD': 'wjbb111',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

LOGIN_URL = '/merchant/login/'

STATIC_URL = '/static/'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending email.
#EMAIL_HOST = 'localhost'
EMAIL_HOST = 'smtp.126.com'
DEFAULT_FROM_EMAIL = 'datateller@126.com'
# Port for sending email.
EMAIL_PORT = 25

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'datateller@126.com'
EMAIL_HOST_PASSWORD = 'wjbb111'
EMAIL_USE_TLS = True

#DATABASE_ROUTERS = ['ywbweb.dbrouter.DBRouter',]
