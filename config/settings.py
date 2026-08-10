"""
Pacita Tianna — site backend (Django admin + REST API).

Every value that differs between environments is read from environment
variables (a local .env file is supported via python-dotenv). See .env.example.
"""
from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def env_bool(name: str, default: bool = False) -> bool:
    return env(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


# ── Core ─────────────────────────────────────────────
SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-secret-key-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", "*").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in env("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    # site apps
    "content",
    "shop",
    "gallery",
    "orders",
    "lulu_api",
    "inbox",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# MySQL in production (PythonAnywhere), SQLite locally.
if env("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
            # PythonAnywhere drops idle MySQL connections after ~5 minutes,
            # so keep them short-lived and health-checked.
            "CONN_MAX_AGE": 60,
            "CONN_HEALTH_CHECKS": True,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
# For Postgres in production, set DATABASE_URL-style env vars and swap here,
# or simply replace the block above:
#   "ENGINE": "django.db.backends.postgresql", "NAME": env("PG_NAME"), ...

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Los_Angeles"  # Las Vegas
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── REST framework ───────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "UNAUTHENTICATED_USER": None,
}

# ── CORS (the React site calls this API) ─────────────
CORS_ALLOWED_ORIGINS = [o.strip() for o in env("CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if o.strip()]
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL_ORIGINS", False)

# ── Square ───────────────────────────────────────────
SQUARE_ACCESS_TOKEN = env("SQUARE_ACCESS_TOKEN")
SQUARE_LOCATION_ID = env("SQUARE_LOCATION_ID")
SQUARE_ENVIRONMENT = env("SQUARE_ENVIRONMENT", "sandbox")  # "sandbox" | "production"
SQUARE_WEBHOOK_SIGNATURE_KEY = env("SQUARE_WEBHOOK_SIGNATURE_KEY")
SQUARE_WEBHOOK_NOTIFICATION_URL = env("SQUARE_WEBHOOK_NOTIFICATION_URL")  # exact URL registered in Square
SQUARE_REDIRECT_URL = env("SQUARE_REDIRECT_URL", "https://www.pacitatiana.com/thank-you")

# ── Lulu Print API ───────────────────────────────────
LULU_CLIENT_KEY = env("LULU_CLIENT_KEY")
LULU_CLIENT_SECRET = env("LULU_CLIENT_SECRET")
LULU_USE_SANDBOX = env_bool("LULU_USE_SANDBOX", True)
LULU_CONTACT_EMAIL = env("LULU_CONTACT_EMAIL", "hello@pacitatiana.com")
# 6x9 (0600X0900) B&W standard perfect-bound is typical for The Appointed Time.
# TODO: confirm the exact pod_package_id in the Lulu portal price calculator.
LULU_POD_PACKAGE_ID = env("LULU_POD_PACKAGE_ID", "0600X0900.BW.STD.PB.060UW444.G")
LULU_SHIPPING_LEVEL = env("LULU_SHIPPING_LEVEL", "MAIL")  # MAIL|PRIORITY_MAIL|GROUND|EXPEDITED|EXPRESS
# URLs Lulu downloads the book files from (private, stable URLs):
LULU_INTERIOR_URL = env("LULU_INTERIOR_URL")
LULU_COVER_URL = env("LULU_COVER_URL")
# When True, a paid Square order containing the paperback automatically
# creates a Lulu print job from the webhook:
LULU_AUTO_PRINT = env_bool("LULU_AUTO_PRINT", False)

# ── Mailchimp (newsletter audience sync) ─────────────
MAILCHIMP_API_KEY = env("MAILCHIMP_API_KEY")  # e.g. abc123...-us21
MAILCHIMP_LIST_ID = env("MAILCHIMP_LIST_ID")  # Audience ID from Mailchimp settings
MAILCHIMP_DOUBLE_OPT_IN = env_bool("MAILCHIMP_DOUBLE_OPT_IN", False)

# ── EmailJS (order + form notifications to Pacita) ───
EMAILJS_SERVICE_ID = env("EMAILJS_SERVICE_ID")
EMAILJS_PUBLIC_KEY = env("EMAILJS_PUBLIC_KEY")
EMAILJS_PRIVATE_KEY = env("EMAILJS_PRIVATE_KEY")
EMAILJS_ORDER_TEMPLATE_ID = env("EMAILJS_ORDER_TEMPLATE_ID", "new_order")

# sent to the BUYER after payment, carrying their eBook download links
EMAILJS_DELIVERY_TEMPLATE_ID = env("EMAILJS_DELIVERY_TEMPLATE_ID", "ebook_delivery")
EBOOK_LINK_NOTE = env("EBOOK_LINK_NOTE", "These links are yours to keep — save the files somewhere safe.")