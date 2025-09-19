from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

# โหลด .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- Core envs ----
SECRET_KEY = os.getenv('SECRET_KEY', 'replace-me')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ---- ALLOWED_HOSTS ----
hosts_env = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in hosts_env.split(',') if h.strip()]

# สำหรับ dev / production defaults
default_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]
if not DEBUG:
    default_hosts.append("anime-diary.onrender.com")

ALLOWED_HOSTS += default_hosts
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))  # ลบ host ซ้ำ

# ---- CSRF_TRUSTED_ORIGINS ----
csrf_env = os.getenv('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = []

for origin in csrf_env.split(','):
    origin = origin.strip()
    if origin:
        # ถ้าไม่มี scheme ให้เติม https:// เป็น default
        if not origin.startswith('http://') and not origin.startswith('https://'):
            origin = 'https://' + origin
        CSRF_TRUSTED_ORIGINS.append(origin)

# dev localhost
if DEBUG:
    CSRF_TRUSTED_ORIGINS += [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

# production domain
prod_domain = "https://anime-diary.onrender.com"
if not DEBUG and prod_domain not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(prod_domain)

CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))  # ลบซ้ำ

# ---- Django / allauth ----
SITE_ID = int(os.getenv('SITE_ID', '2'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_general.apps.AppGeneralConfig',
    'app_myanimes.apps.AppMyanimesConfig',
    'app_users.apps.AppUsersConfig',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
    "django_extensions",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'ProjectAnimeDiary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'app_general' / 'templates',
            BASE_DIR / 'app_myanimes' / 'templates',
            BASE_DIR / 'app_users' / 'templates',
        ],
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

WSGI_APPLICATION = 'ProjectAnimeDiary.wsgi.application'

# ---- Database ----
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite'}",
        conn_max_age=600,  # สำหรับ connection pooling บน Render
    )
}

# ---- Password validators ----
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---- i18n / tz ----
LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# ---- Static / Media ----
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---- allauth ----
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

ACCOUNT_EMAIL_VERIFICATION = 'none'

# ✅ ใช้ login ได้ทั้ง username + email
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    },
    'github': {
        'SCOPE': ['user', 'user:email'],
    },
}
