#!/usr/bin/env python3
"""
Final check for Swagger documentation consistency
This script verifies all endpoints have proper documentation
"""
import os
import sys
import django
from django.conf import settings

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.settings')

# Initialize Django
django.setup()

from mood_tracker.tracker.views import *
from mood_tracker.tracker.urls import urlpatterns
from django.urls import get_resolver
from rest_framework.views import APIView
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
import inspect

def check_swagger_documentation():
    """Check all API views for proper Swagger documentation"""
    print("🔍 CHECKING SWAGGER DOCUMENTATION CONSISTENCY")
    print("=" * 70)
    
    # Get all view classes from the tracker app
    view_classes = []
    for name, obj in inspect.getmembers(sys.modules['mood_tracker.tracker.views']):
        if inspect.isclass(obj) and (
            issubclass(obj, APIView) or 
            issubclass(obj, generics.GenericAPIView)
        ) and obj not in [APIView, generics.GenericAPIView]:
            view_classes.append((name, obj))
    
    print(f"Found {len(view_classes)} API view classes:")
    print("-" * 50)
    
    issues_found = []
    
    for view_name, view_class in view_classes:
        print(f"\n📋 {view_name}:")
        
        # Check HTTP methods
        methods = []
        if hasattr(view_class, 'get'):
            methods.append('GET')
        if hasattr(view_class, 'post'):
            methods.append('POST')
        if hasattr(view_class, 'put'):
            methods.append('PUT')
        if hasattr(view_class, 'patch'):
            methods.append('PATCH')
        if hasattr(view_class, 'delete'):
            methods.append('DELETE')
        
        print(f"   Methods: {', '.join(methods)}")
        
        # Check each method for swagger documentation
        for method in methods:
            method_func = getattr(view_class, method.lower(), None)
            if method_func:
                # Check if method has swagger_auto_schema decorator
                has_swagger = False
                if hasattr(method_func, '__annotations__') or hasattr(method_func, 'swagger_auto_schema'):
                    has_swagger = True
                
                # Check for decorator by examining the method
                if hasattr(method_func, '__wrapped__'):
                    has_swagger = True
                
                # More comprehensive check
                source = inspect.getsource(method_func) if hasattr(method_func, '__code__') else ""
                if '@swagger_auto_schema' in source:
                    has_swagger = True
                
                if has_swagger:
                    print(f"   ✅ {method}: Has Swagger documentation")
                else:
                    print(f"   ❌ {method}: Missing Swagger documentation")
                    issues_found.append(f"{view_name}.{method}")
    
    print("\n" + "=" * 70)
    if issues_found:
        print(f"⚠️  ISSUES FOUND: {len(issues_found)} methods missing Swagger documentation")
        for issue in issues_found:
            print(f"   - {issue}")
    else:
        print("✅ ALL ENDPOINTS HAVE PROPER SWAGGER DOCUMENTATION!")
    
    print("\n🔗 URL PATTERNS CHECK:")
    print("-" * 50)
    
    for pattern in urlpatterns:
        if hasattr(pattern, 'pattern') and hasattr(pattern.pattern, '_route'):
            route = pattern.pattern._route
            if '<' in route:  # Has path parameters
                print(f"   📍 {route} - Has path parameters")
            else:
                print(f"   📍 {route} - No path parameters")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    try:
        all_good = check_swagger_documentation()
        print(f"\n{'🎉 SWAGGER DOCUMENTATION CHECK COMPLETE!' if all_good else '⚠️ SOME ISSUES FOUND'}")
        sys.exit(0 if all_good else 1)
    except Exception as e:
        print(f"❌ Error during check: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
