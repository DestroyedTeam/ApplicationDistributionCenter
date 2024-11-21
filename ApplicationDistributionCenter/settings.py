"""
Django settings for ApplicationDistributionCenter project.

"""

import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = ["*", "0.0.0.0"]

# Application definition
INSTALLED_APPS = [
    "simpleui",
    "import_export",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "testunit.apps.TestunitConfig",
    "analytics.apps.AnalyticsConfig",
    "announcements.apps.AnnouncementsConfig",
    "category.apps.CategoryConfig",
    "comments.apps.CommentsConfig",
    "articles.apps.ArticlesConfig",
    "favorites.apps.FavoritesConfig",
    "visitor.apps.VisitorConfig",
    "questions.apps.QuestionsConfig",
    "software.apps.SoftwareConfig",
    "error_handler.apps.ErrorHandlerConfig",
    "components.apps.ComponentsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "personal_components.append_middleware.AppendMiddleware",
]

ROOT_URLCONF = "ApplicationDistributionCenter.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "ApplicationDistributionCenter.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "PORT": env("POSTGRES_PORT"),
        "HOST": env("POSTGRES_HOST"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "NAME": env("POSTGRES_DATABASE"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "DECODE_RESPONSE": True,
            "PASSWORD": env("REDIS_PASSWORD") if env("REDIS_PASSWORD") else None,
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "PRC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
if env("DEBUG", default=True):
    # NOTE: STATICFILES_DIRS is only used in development
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    # NOTE: STATIC_ROOT is only used in production
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Additional Config
GZIP_MIN_LENGTH = 500  # GZip middleware min length

# simpleui that backend settings
SIMPLEUI_HOME_PAGE = "/analytics/backstage-overview"
SIMPLEUI_HOME_TITLE = "概览"
SIMPLEUI_LOGO = "/static/favicon.ico"  # left top logo
SIMPLEUI_DEFAULT_THEME = "e-purple.css"  # default theme
SIMPLEUI_HOME_INFO = False  # disabled home page info in the backend
LOGIN_URL = "/login/"  # login url
