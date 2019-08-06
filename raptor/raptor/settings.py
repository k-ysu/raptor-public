"""
Django settings for raptor project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import socket
import os

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# SERVER CONF, debug or prod
SERVER_CONF = 'debug'
if IPAddr == '0.0.0.0': # Fake
    SERVER_CONF = 'prod'
elif IPAddr == '0.0.0.0': # Fake
    SERVER_CONF = 'prod'

# SERVER SERVICE, jp or global
SERVER_SERVICE = 'jp'
if IPAddr == '0.0.0.0': # Fake
    SERVER_SERVICE = 'jp'
elif  IPAddr == '0.0.0.0': # Fake
    SERVER_SERVICE = 'global'
elif SERVER_CONF == 'debug':
    SERVER_SERVICE = 'global'

#For Debug
#SERVER_SERVICE = 'jp'
#SERVER_CONF = 'prod'

print("=== SERVER_CONF : {} ===".format(SERVER_CONF))
print("=== SERVER_SERVICE : {} ===".format(SERVER_SERVICE))
print("=== HOSTNAME : {} ===".format(hostname))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-(kj)fcbivggc-huf+v8$zk**!+5sg$40(igkoc1hiku6)5m4b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0']
if SERVER_CONF == 'prod':
    DEBUG = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'streamer.apps.StreamerConfig',
    'django.contrib.humanize',
    'debug_toolbar',
    'bootstrap4',
    'django_user_agents',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

#Setting for sitemaps
SITE_ID = 1


''' # Disable Cache for now => https://github.com/selwin/django-user_agents
# Cache backend is optional, but recommended to speed up user agent parsing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
USER_AGENTS_CACHE = 'default'
'''



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware', # This will allows user to switch language, I want to force user to use our native language
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'raptor.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'raptor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if SERVER_SERVICE == 'jp':

    DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #    }
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fake',  # Database名
            'USER': 'fake',  # ユーザID
            'PASSWORD': 'fake',  # ユーザIDのパスワード
            'HOST': 'fake',  # ホスト名、別のホストを指定する場合は「xxx.xxx.xxx.xxx」のようにIPアドレスで指定できる
            'PORT': 'fake',
        }

    }

elif SERVER_SERVICE == 'global':

    DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.sqlite3',
    #        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #    }
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fake',  # Database名
            'USER': 'fake',  # ユーザID
            'PASSWORD': 'fake',  # ユーザIDのパスワード
            'HOST': 'fake',  # ホスト名、別のホストを指定する場合は「xxx.xxx.xxx.xxx」のようにIPアドレスで指定できる
            'PORT': 'fake',
        }

    }



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

if SERVER_SERVICE == 'jp':

    LANGUAGE_CODE = 'ja'

elif SERVER_SERVICE == 'global':

    LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
INTERNAL_IPS = ['127.0.0.1']
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)