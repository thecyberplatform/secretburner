# ---------------------------------------------------------------------------------------------------------------------
#                                           _     _
#                    ___  ___  ___ _ __ ___| |_  | |__  _   _ _ __ _ __   ___ _ __
#                   / __|/ _ \/ __| '__/ _ \ __| | '_ \| | | | '__| '_ \ / _ \ '__|
#                   \__ \  __/ (__| | |  __/ |_  | |_) | |_| | |  | | | |  __/ |
#                   |___/\___|\___|_|  \___|\__| |_.__/ \__,_|_|  |_| |_|\___|_|
#
#                                        Django Configuration
#
#                      Most settings should be changed in your env file, not here.
#
# ---------------------------------------------------------------------------------------------------------------------

import datetime
import sys
from pathlib import Path

import environ

ROOT_DIR = environ.Path(__file__) - 2
CONFIG_DIR = environ.Path(__file__) - 1

# ---------------------------------------------------------------------------------------------------------------------
# Load operating system environment variables and then prepare to use them
# ---------------------------------------------------------------------------------------------------------------------
env = environ.Env()

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------------------------------------------------
# Security Configuration
# ---------------------------------------------------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
USE_PG_CRON = env.bool("USE_PG_CRON", default=True)

# ---------------------------------------------------------------------------------------------------------------------
# Debug settings
# ---------------------------------------------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG")
DEBUG_DB = env.bool("DEBUG_DB", default=False)

# ---------------------------------------------------------------------------------------------------------------------
# Application Settings
# ---------------------------------------------------------------------------------------------------------------------
APP_NAME = env("APP_NAME")
API_HOSTNAME = env("API_HOSTNAME")
UI_HOSTNAME = env("UI_HOSTNAME")

UI_FULFIL_REQUEST_URI = env("UI_FULFIL_REQUEST_URI")
UI_VIEW_SECRET_URL = env("UI_VIEW_SECRET_URL")

# ---------------------------------------------------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------------------------------------------------
ALLOW_EMAIL = env.bool("ALLOW_EMAIL")
EMAIL_VERIFICATION_EXPIRY_SECONDS = env.int("EMAIL_VERIFICATION_EXPIRY_SECONDS")
REQUIRE_VERIFICATION = env.bool("REQUIRE_VERIFICATION")
MAIL_ESP = env("MAIL_ESP")
ESP_API_KEY = env("ESP_API_KEY")
MAILER_FROM_EMAIL = env("MAILER_FROM_EMAIL")
MAILER_REPLY_TO_EMAIL = env("MAILER_REPLY_TO_EMAIL")

if ALLOW_EMAIL and MAIL_ESP not in [
    "sendgrid",
    "mandrill",
    "mailgun",
    "brevo",
    "mailsend",
    "postal",
    "postmark",
    "resend",
    "sparkpost",
]:
    raise Exception("Unsupported Mail ESP, env: MAIL_ESP")

EMAIL_BACKEND = f"anymail.backends.{MAIL_ESP}.EmailBackend"

ANYMAIL = {
    "SENDGRID_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "sendgrid" else None,
    "MAILGUN_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "mailgun" else None,
    "MANDRILL_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "mandrill" else None,
    "BREVO_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "brevo" else None,
    "MAILERSEND_API_TOKEN": env("ESP_API_KEY") if MAIL_ESP == "mailsend" else None,
    "POSTAL_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "postal" else None,
    "POSTMARK_SERVER_TOKEN": env("ESP_API_KEY") if MAIL_ESP == "postmark" else None,
    "RESEND_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "resend" else None,
    "SPARKPOST_API_KEY": env("ESP_API_KEY") if MAIL_ESP == "sparkpost" else None,
}

# ---------------------------------------------------------------------------------------------------------------------
# Cache Configuration
# ---------------------------------------------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": env("CACHE_BACKEND"),
        "LOCATION": env("CACHE_LOCATION"),
    }
}

if env("CACHE_CLIENT_CLASS", default=None) is not None:
    CACHES["default"]["OPTIONS"] = {"CACHE_CLIENT_CLASS": env("CACHE_CLIENT_CLASS")}

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "rest_framework",
    "core.base",
    "secret",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.base.middleware.data.ConvertRequestEmptyStringToNull",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(ROOT_DIR("")),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------------------------------------------------------
# API Configuration
# ---------------------------------------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "EXCEPTION_HANDLER": "core.base.exception_handler.exception_handler.custom_exception_handler",
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
        "ignore_fields": ["tags", "metadata"],
    },
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}

if env.bool("APPLY_PER_VIEW_THROTTLING", default=False) is True:
    REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"].append(
        "core.base.api.throttling.AnonRateThrottlePerView"
    )
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["anon_per_view"] = env(
        "PER_VIEW_THROTTLE_RATE", default="20/day"
    )

# ---------------------------------------------------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DBNAME"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
    },
}

# ---------------------------------------------------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------------------------------------------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ---------------------------------------------------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------------------------------------------------
_LOG_HANDLERS = ["console"]

if TESTING:
    _LOG_HANDLERS = ["null"]

LOGGING = {
    "version": 1,
    "filters": {},
    "formatters": {},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": [],
        },
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": _LOG_HANDLERS,
            "propagate": True,
            "level": "INFO",
        },
    },
}

# ---------------------------------------------------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# ---------------------------------------------------------------------------------------------------------------------
STATIC_DIRECTORY = "static"
STATICFILES_DIRS = []

STATIC_ROOT = str(ROOT_DIR("static"))
STATIC_URL = "/static/"

# ---------------------------------------------------------------------------------------------------------------------
# Media configuration
# ---------------------------------------------------------------------------------------------------------------------
MEDIA_DIRECTORY = "media"

MEDIA_ROOT = str(ROOT_DIR("media"))
MEDIA_URL = "/media/"

# THESE CONFIGURATION SETTINGS ARE REQUIRED BY DJANGO, BUT NOT USE IN THIS PROJECT
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

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

# ---------------------------------------------------------------------------------------------------------------------
# Session expiry settings - the below are defaults for login with 'remember me' turned on
# ---------------------------------------------------------------------------------------------------------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # One month
SESSION_COOKIE_SAMESITE = None

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ---------------------------------------------------------------------------------------------------------------------
# DO NOT EDIT BELOW HERE
# ---------------------------------------------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
