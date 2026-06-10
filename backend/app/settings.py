import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev_secret")
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.postgres",
    "rest_framework",
    "app.apps.products",
    "app.apps.orders",
    "app.apps.points",
    "app.apps.reviews",
    "app.apps.notifications",
    "app.apps.users",
]
MIDDLEWARE = ["django.middleware.common.CommonMiddleware", "django.contrib.sessions.middleware.SessionMiddleware"]
ROOT_URLCONF = "app.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "cycleapi"),
        "USER": os.getenv("POSTGRES_USER", "cycle_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "cycle_pass"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "EXCEPTION_HANDLER": "app.middleware.exception_handler.standard_exception_handler",
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
