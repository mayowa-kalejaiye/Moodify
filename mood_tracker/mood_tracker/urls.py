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
# Import the token view properly
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create schema view for API documentation with explicit public access
@method_decorator(csrf_exempt, name='dispatch')
class PublicSchemaView:
    """Custom wrapper to ensure schema views are always public"""
    pass

schema_view = get_schema_view(
    openapi.Info(
        title="MoodSync API",
        default_version='v1',
        description="AI-powered mood tracking and wellness platform with time-conscious insights",
        terms_of_service="https://github.com/mayowa-kalejaiye/Moodify",
        contact=openapi.Contact(email="contact@moodsync.app"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],  # Explicitly no authentication for docs
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API documentation with Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
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


