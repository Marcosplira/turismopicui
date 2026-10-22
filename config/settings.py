"""
Django settings for config project.
"""

import os
from pathlib import Path
import dj_database_url

# ==========================================================
# CAMINHOS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# SEGURANÇA
# ==========================================================
# Aceita tanto DEBUG quanto DJANGO_DEBUG, e por padrão é True no local
DEBUG = (
    os.environ.get("DEBUG", os.environ.get("DJANGO_DEBUG", "True")).lower() == "true"
)

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-picui-turismo-dev-local-123456789"
    else:
        # Em produção vai precisar definir a variável no Render
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured("Defina DJANGO_SECRET_KEY em produção.")

# ==========================================================
# HOSTS PERMITIDOS
# ==========================================================
ALLOWED_HOSTS = [
    "turismo.picui.pb.gov.br",
    "www.turismo.picui.pb.gov.br",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

# Se você estiver usando variável de ambiente para complementar, ela continuará funcionando:
extra_hosts = os.environ.get("ALLOWED_HOSTS", "")
if extra_hosts:
    for host in extra_hosts.split(","):
        if host.strip() and host.strip() not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host.strip())

if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(os.environ["RENDER_EXTERNAL_HOSTNAME"])

# ==========================================================
# CSRF
# ==========================================================
CSRF_TRUSTED_ORIGINS = [
    "https://turismo.picui.pb.gov.br",
    "https://www.turismo.picui.pb.gov.br",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]

if os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}")

# ==========================================================
# APLICAÇÕES
# ==========================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cadastro",
]

# ==========================================================
# MIDDLEWARE
# ==========================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==========================================================
# URL / TEMPLATES
# ==========================================================
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ==========================================================
# BANCO DE DADOS
# ==========================================================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ==========================================================
# VALIDAÇÃO DE SENHA
# ==========================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==========================================================
# INTERNACIONALIZAÇÃO
# ==========================================================
LANGUAGE_CODE = "pt-BR"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True

# ==========================================================
# ARQUIVOS ESTÁTICOS
# ==========================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
ANDROID_PACKAGE_NAME = os.environ.get("ANDROID_PACKAGE_NAME", "com.turismopicui.guia")
ANDROID_SHA256_CERT_FINGERPRINT = os.environ.get("ANDROID_SHA256_CERT_FINGERPRINT", "")

# ==========================================================
# ARQUIVOS DE MÍDIA
# ==========================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==========================================================
# CONFIGURAÇÃO DE E-MAIL
# ==========================================================
if DEBUG:
    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.console.EmailBackend",
        },
    }
else:
    MAILERS = {
        "default": {
            "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
            "OPTIONS": {
                "host": os.environ.get("EMAIL_HOST", "smtp.gmail.com"),
                "port": int(os.environ.get("EMAIL_PORT", "587")),
                "username": os.environ.get("EMAIL_HOST_USER", ""),
                "password": os.environ.get("EMAIL_HOST_PASSWORD", ""),
                "use_tls": os.environ.get("EMAIL_USE_TLS", "True").lower() == "true",
            },
        },
    }

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "Turismo de Picuí <turismopicui@gmail.com>",
)

ADMIN_EMAIL = os.environ.get(
    "ADMIN_EMAIL",
    "admin@prefeiturapicui.gov.br",
)

# ==========================================================
# PADRÃO
# ==========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
