"""
URL Configuration for mood_tracker project.
"""

# Import all URLs from the inner URLs file
from mood_tracker.mood_tracker.urls import *

from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),  # Include tracker app URLs
    # Removed accounts/ URLs to prevent login redirects for API documentation
    # path('accounts/', include('django.contrib.auth.urls')),  # Includes default auth URLs
    
]


