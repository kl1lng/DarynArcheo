import os
from pathlib import Path

# Построение путей внутри проекта (archaeology/settings.py -> archaeology -> root)
BASE_DIR = Path(__file__).resolve().parent.parent

# БЕЗОПАСНОСТЬ
SECRET_KEY = 'django-insecure-your-key-here' # В будущем замени на переменную окружения
DEBUG = True  # Для разработки. На продакшене ставь False
ALLOWED_HOSTS = ['kazarcheo.pythonanywhere.com', '127.0.0.1', 'localhost']

# ПРИЛОЖЕНИЯ
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'archaeology', # Твое основное приложение
]

# ПРОМЕЖУТОЧНОЕ ПО
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'archaeology.urls'

# ШАБЛОНЫ
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'archaeology.wsgi.application'

# БАЗА ДАННЫХ
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ВАЛИДАЦИЯ ПАРОЛЕЙ (Отключена для удобства разработки)
AUTH_PASSWORD_VALIDATORS = []

# ИНТЕРНАЦИОНАЛИЗАЦИЯ
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("ru", "Русский"),
    ("kk", "Қазақша"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Здесь Django ищет файлы ПЕРЕД сборкой (collectstatic)
STATICFILES_DIRS = [
    # Если у тебя есть папка static в корне проекта, раскомментируй строку ниже:
    # BASE_DIR / "static", 
]

# МЕДИА ФАЙЛЫ (Загрузки пользователей, 3D-модели)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Поля по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"