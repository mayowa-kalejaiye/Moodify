"""
URL configuration for mood_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

# Import our custom public Swagger views
from mood_tracker.tracker.swagger_views import (
    public_swagger_ui, 
    public_redoc_ui, 
    public_swagger_json
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation - COMPLETELY PUBLIC, using custom views with ZERO authentication
    path('swagger<format>/', public_swagger_json, name='schema-json'),
    path('swagger/', public_swagger_ui, name='schema-swagger-ui'),
    path('redoc/', public_redoc_ui, name='schema-redoc'),
    
    # Add direct token auth endpoint
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    # Include tracker app urls
    path('', include('mood_tracker.tracker.urls')),
]

# For development environment, add DRF browsable API authentication
from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]


