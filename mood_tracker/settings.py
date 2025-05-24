"""
Django settings for mood_tracker project.
"""

# Import all settings from the inner settings file
from mood_tracker.mood_tracker.settings import *

# You can override specific settings here if needed
# For production environments
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
