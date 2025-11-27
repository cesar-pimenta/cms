# config/local_settings_example.py
# Exemplo de configurações locais para desenvolvimento

# Copie este arquivo para config/local_settings.py e customize conforme necessário

# DEBUG
DEBUG = True

# Hosts permitidos
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database - Padrão é SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

# Se preferir usar PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'portal_noticias',
#         'USER': 'postgres',
#         'PASSWORD': 'senha',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Se preferir usar MySQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'portal_noticias',
#         'USER': 'root',
#         'PASSWORD': 'senha',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# Email - Para desenvolvimento, use console backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para produção com Gmail:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'seu-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'sua-senha-de-aplicativo'
# DEFAULT_FROM_EMAIL = 'seu-email@gmail.com'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'portal.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Cache - Para desenvolvimento usar locmem
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'portal-cache',
    }
}

# Para produção com Redis:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }

# Cookies
SESSION_COOKIE_SECURE = False  # True em produção com HTTPS
CSRF_COOKIE_SECURE = False     # True em produção com HTTPS
SECURE_SSL_REDIRECT = False    # True em produção com HTTPS

# Timezone
TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True

# Uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Customizações da aplicação
ITEMS_PER_PAGE = 12
SEARCH_LIMIT = 100
MAX_IMAGES_PER_EDITORIAL = 3
MAX_TEMAS_PER_EDITORIAL = 10
