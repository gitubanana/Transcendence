"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os

# 프로젝트에서 사용될 사용자 모델 지정
AUTH_USER_MODEL = 'users.User'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qd%5r=g1i8lcexi$x%_h(kg6m3akv59zr6ziosita=pqkcc6+)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ['https://localhost:5000', 'https://127.0.0.1:5000']

# ALLOWED_HOSTS = ['django']
# ALLOWED_HOSTS = ['django', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'users',
    'matches',
    'pongGame',
    'relationships',
	'django_prometheus',
]

MIDDLEWARE = [
	'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.tokenCheck',
	'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_CACHE_HOST'), os.environ.get('REDIS_CACHE_PORT'))],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('POSTGRES_DB', 'Transcendence_db'),
        'USER': os.environ.get('POSTGRES_USER', 'Transcendence_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'Transcendence_password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgresql'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

# Media files configuration (Default User Profile image)
MEDIA_URL = 'media/'
MEDIA_ROOT = [BASE_DIR / 'media']

# 기본 이미지 경로 설정
DEFAULT_PROFILE_IMAGE_URL = '/image/profile/default_profile.png'
DEFAULT_TIER_IMAGE_URL = '/images/tier/bronze.svg'
DEFAULT_GAME_SKIN_IMAGE_URL = '/images/game_skin/ping_pong.svg'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs') + "/log.log",
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # 기본 인증 클래스 설정
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # JWT 인증 방식을 사용
        # 들어오는 요청의 Authorization 헤더에서 JWT 토큰을 찾아 사용자를 인증한다
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
SIMPLE_JWT = {
    # ***액세스 토큰의 유효 기간 설정 (예: 5분)
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),

    # ***리프레시 토큰의 유효 기간 설정 (예: 1일)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    # 리프레시 토큰을 갱신할 때마다 새로운 리프레시 토큰 발급 여부
    "ROTATE_REFRESH_TOKENS": False,

    # 리프레시 토큰 회전 후 이전 토큰을 블랙리스트에 추가할지 여부
    "BLACKLIST_AFTER_ROTATION": False,

    # 로그인 시 'last_login' 필드 업데이트 여부
    "UPDATE_LAST_LOGIN": False,

    # ***토큰 서명/검증에 사용할 알고리즘 (예: HS256)
    "ALGORITHM": "HS256",

    # ***토큰 서명에 사용될 키 (Django SECRET_KEY 사용)
    "SIGNING_KEY": SECRET_KEY,

    # 토큰 검증에 사용될 키 (HMAC 사용 시 SIGNING_KEY와 동일)
    "VERIFYING_KEY": "",

    # 토큰의 'aud' 클레임 (None일 경우 토큰에서 제외)
    "AUDIENCE": None,

    # 토큰의 'iss' 클레임 (None일 경우 토큰에서 제외)
    "ISSUER": None,

    # 사용자 정의 JSON 인코더 (None일 경우 기본 인코더 사용)
    "JSON_ENCODER": None,

    # 공개키를 제공하는 JWKS URL (None일 경우 사용 안 함)
    "JWK_URL": None,

    # 토큰 만료 시간에 대한 여유 마진 설정
    "LEEWAY": 0,

    # 인증 헤더 타입 설정 ('Bearer' 사용)
    "AUTH_HEADER_TYPES": ("Bearer",),

    # 인증 헤더 이름 설정 ('Authorization' 사용)
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    # 사용자 식별에 사용될 필드 ('id' 사용)
    "USER_ID_FIELD": "id",

    # 토큰에 포함될 사용자 식별 정보 필드 ('user_id' 사용)
    "USER_ID_CLAIM": "user_id",

    # 사용자 인증 규칙 설정
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    # 인증에 사용될 토큰 클래스 설정
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),

    # 토큰 타입을 나타내는 클레임 이름 설정
    "TOKEN_TYPE_CLAIM": "token_type",

    # 토큰 사용자 클래스 설정
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # 토큰 고유 식별자(JTI) 클레임 이름 설정
    "JTI_CLAIM": "jti",

    # 슬라이딩 토큰 유효 기간 및 리프레시 유효 기간 설정
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    # 토큰 발급 및 갱신 등에 사용될 시리얼라이저 설정
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
