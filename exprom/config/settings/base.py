import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from config.settings.ckeditor import CKEDITOR_CONFIGS


BASE_DIR = Path(__file__).resolve().parent.parent.parent


LOG_FMT = "%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"
LOG_DATE_FMT = "%Y-%m-%d %H:%M:%S"
fmt = logging.Formatter(fmt=LOG_FMT, datefmt=LOG_DATE_FMT)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(fmt)

fh = logging.FileHandler(os.path.join(BASE_DIR, 'info.log'))
fh.setLevel(logging.INFO)
fh.setFormatter(fmt)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(sh)
logger.addHandler(fh)


load_dotenv(os.path.join(BASE_DIR.parent, '.env'))


SECRET_KEY = os.getenv('SECRET_KEY', '')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'apps.fpages',

    'debug_toolbar',
    'ckeditor',

    'apps.catalog.apps.CatalogConfig',
    'apps.mainpage',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ---------------flatpages--------------
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # ---------------flatpages--------------

    # ----------------debug-----------------
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ----------------debug-----------------
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'libraries': {
                'all_pages_tags': 'templatetags.all_pages_tags',
            },
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv('POSTGRESQL_DATABASE'),
        "USER": os.getenv('POSTGRESQL_USER'),
        "PASSWORD": os.getenv('POSTGRESQL_PASSWORD'),
        "HOST": os.getenv('POSTGRESQL_HOST', 'localhost'),
        "PORT": os.getenv('POSTGRESQL_PORT', '5432'),
    }
}

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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
]

CKEDITOR_CONFIGS = CKEDITOR_CONFIGS
