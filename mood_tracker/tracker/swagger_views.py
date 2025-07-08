"""
Custom Swagger views that completely bypass Django authentication
"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json


@csrf_exempt
@never_cache
@require_http_methods(["GET"])
def public_swagger_ui(request):
    """
    Completely public Swagger UI view with zero authentication
    """
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    
    # Create a fresh schema view for this request
    schema_view = get_schema_view(
        openapi.Info(
            title="MoodSync API",
            default_version='v1',
            description="AI-powered mood tracking and wellness platform",
            contact=openapi.Contact(email="contact@moodsync.app"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
        authentication_classes=[],
    )
    
    # Create the view and call it
    view_func = schema_view.with_ui('swagger', cache_timeout=0)
    
    # Remove any authentication from the request
    request.user = None
    request.auth = None
    
    return view_func(request)


@csrf_exempt
@never_cache
@require_http_methods(["GET"])
def public_redoc_ui(request):
    """
    Completely public ReDoc UI view with zero authentication
    """
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    
    # Create a fresh schema view for this request
    schema_view = get_schema_view(
        openapi.Info(
            title="MoodSync API",
            default_version='v1',
            description="AI-powered mood tracking and wellness platform",
            contact=openapi.Contact(email="contact@moodsync.app"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
        authentication_classes=[],
    )
    
    # Create the view and call it
    view_func = schema_view.with_ui('redoc', cache_timeout=0)
    
    # Remove any authentication from the request
    request.user = None
    request.auth = None
    
    return view_func(request)


@csrf_exempt
@never_cache
@require_http_methods(["GET"])
def public_swagger_json(request, format='.json'):
    """
    Completely public Swagger JSON schema with zero authentication
    """
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    
    # Create a fresh schema view for this request
    schema_view = get_schema_view(
        openapi.Info(
            title="MoodSync API",
            default_version='v1',
            description="AI-powered mood tracking and wellness platform",
            contact=openapi.Contact(email="contact@moodsync.app"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
        authentication_classes=[],
    )
    
    # Create the view and call it
    view_func = schema_view.without_ui(cache_timeout=0)
    
    # Remove any authentication from the request
    request.user = None
    request.auth = None
    
    return view_func(request, format=format)
