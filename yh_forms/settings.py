from pathlib import Path
import os
import django.core.exceptions
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


ALLOWED_HOSTS = ["*"]

# Custom wrapper in order to handle os environment variables errors
# ref. https://djangostars.com/blog/configuring-django-settings-best-practices/

from django.core.exceptions import ImproperlyConfigured


def get_value(env_variable, default=None):
    """
    Retrieves an environment variable securely, searching in the following order:

    1. Environment variables (os.environ)
    2. .env file (if the file exists)

    Raises an ImproperlyConfigured exception if the variable is not found
    in any of these locations.

    Args:
        env_variable: The name of the environment variable to retrieve.
        default: An optional default value to return if the variable is not found.

    Returns:
        The value of the environment variable or the provided default value
        if not found. Raises an ImproperlyConfigured exception if the variable
        is not found and no default is provided.
    """

    try:
        return os.environ[env_variable]
    except KeyError:
        if default is not None:
            return default
        error_msg = "!! Set the {} environment variable or create a .env file with it.".format(
            env_variable
        )
        raise ImproperlyConfigured(error_msg)


# Every environment will use different seceret key
SECRET_KEY = get_value("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_value("DEBUG")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "base",
    "rest_framework",
    "corsheaders",
    "django_filters",
    "crispy_forms",
    "django_pivot",
    "django_tables2",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "yh_forms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# A list of trusted origins for unsafe requests
CSRF_TRUSTED_ORIGINS = [get_value("CSRF_TRUSTED_ORIGINS")]


WSGI_APPLICATION = "yh_forms.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

import dj_database_url

_DATABASE_URL = get_value("DATABASE_URL", default="")
if _DATABASE_URL:
    DATABASES = {"default": dj_database_url.config(default=_DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": get_value("DB_ENGINE"),
            "NAME": "trbp",
            "USER": get_value("DATABASE_USER"),
            "PASSWORD": get_value("DATABASE_PASS"),
            "HOST": get_value("DB_HOST"),
            "PORT": "5432",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
# STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.request",)

# SMTP CONFIGURATION
SENDGRID_API_KEY = get_value("SENDGRID_API_KEY", default="")
if SENDGRID_API_KEY:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_USER = "apikey"
    EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
    DEFAULT_FROM_EMAIL = env("FROM_EMAIL", default="admin@em9952.yellowhd.com")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
