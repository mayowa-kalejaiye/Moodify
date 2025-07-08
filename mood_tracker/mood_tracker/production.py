from .settings import *

# Production-specific settings
DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# Allow Swagger UI to be embedded (less restrictive for API documentation)
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Changed from 'DENY' to allow Swagger UI

# Ensure your domain is included in allowed hosts
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
else:
    # Default production hosts
    ALLOWED_HOSTS = [
        'moodify-wmcd.onrender.com',
        '.onrender.com',
        'localhost',
        '127.0.0.1'
    ]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = False
cors_origins_env = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(',') if origin.strip()]
else:
    # Default production CORS origins
    CORS_ALLOWED_ORIGINS = [
        "https://moodify-wmcd.onrender.com",
        "https://www.moodify-wmcd.onrender.com",
    ]

# Set up proper logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/mood_tracker.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Configure Redis cache if available
# Uncomment when Redis is configured
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': os.environ.get('REDIS_URL'),
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

# Add whitenoise for static file serving
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure Swagger UI static files are served correctly
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Additional CORS settings for production API access
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
