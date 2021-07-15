import os
from pathlib import Path
import bcrypt
import django_heroku
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'django-insecure-^yk0a#!!l^ozzxqn_nk#pa2gji&r=502auurnh5zd605@d@2ln'

ACCESS_SECRET_KEY = '+gs88jj41i#v(##0^+v)$xmvfoo(cazi))l-7&e9w32-n3j(bw'
# REFRESH_SECRET_KEY = 'nsl7(*i^0z!xj0wy58hq)lda42esc-p%o@x&8av80^vzlaqf5j'

IDENTIFICATION_KEY = '@)0xs2)&by1z9b0yay_4n7y!45y2k(=zqypay%=bn&0n3pk^t8'

SALT = b'$2b$12$7J13G4g/tzi1Kh7C2PrdaO'  # TODO: сделать несколько солей на каждую из групп

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['http://localhost:3000']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend',
    'rest_framework',
    'corsheaders',
    'cloudinary',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'kzenergy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'kzenergy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kzenergy_db',
        'USER': 'postgres',
        'PASSWORD': '788556',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

import dj_database_url

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())

INTERNAL_IPS = [
    '127.0.0.1',
]

cloudinary.config(
    cloud_name="dmh0ekjaw",
    api_key="963345615946785",
    api_secret="JqFaq0KIFuk6rx-Z8eJSK-Gfpgc",
)
