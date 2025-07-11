from .settings import *

# Production-specific settings
DEBUG = False

# Security settings (temporarily relaxed for static file debugging)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# Temporarily allow framing for Swagger UI
X_FRAME_OPTIONS = 'SAMEORIGIN'

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

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Don't use compressed storage for now to avoid issues
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

# Configure whitenoise to serve drf-yasg static files properly
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['js', 'css', 'map', 'json']

# Database configuration for production
# Optimized for Supabase PostgreSQL
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Parse Supabase/PostgreSQL connection
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL, 
            conn_max_age=600,  # Connection pooling
            ssl_require=True   # Ensure SSL for security
        )
    }
    
    # Supabase-specific optimizations
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'require',
        'connect_timeout': 30,
        'application_name': 'moodify_django',
    }
    
    print("🚀 Production: Using Supabase PostgreSQL database")
else:
    # Fallback to SQLite (not recommended for production)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',  # Use /tmp for writable location on Render
        }
    }
    
    print("⚠️  Production: Using SQLite fallback (set DATABASE_URL for Supabase)")
