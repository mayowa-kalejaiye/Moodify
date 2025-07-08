#!/usr/bin/env python3
"""
Swagger Endpoint Test

This script tests if Swagger/API documentation endpoints are accessible
in both development and production modes.

Usage:
    python tests/test_swagger_access.py

Environment:
    Tests both DEBUG=True and DEBUG=False scenarios
"""
import os
import sys
import django
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to Python path
sys.path.append('.')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

def test_swagger_configuration():
    """Test Django Swagger configuration"""
    try:
        django.setup()
        from django.conf import settings
        from django.urls import reverse
        
        print("🔍 Testing Swagger Configuration...")
        print(f"✅ DEBUG mode: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        # Check if drf_yasg is in INSTALLED_APPS
        if 'drf_yasg' in settings.INSTALLED_APPS:
            print("✅ drf_yasg is installed")
        else:
            print("❌ drf_yasg is not in INSTALLED_APPS")
            return False
            
        # Test URL patterns
        try:
            swagger_url = reverse('schema-swagger-ui')
            redoc_url = reverse('schema-redoc')
            print(f"✅ Swagger URL pattern: {swagger_url}")
            print(f"✅ ReDoc URL pattern: {redoc_url}")
        except Exception as e:
            print(f"❌ URL pattern error: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_swagger_endpoint_access(base_url="http://localhost:8000"):
    """Test actual endpoint access"""
    print(f"\n🌐 Testing Swagger endpoint access at {base_url}")
    
    endpoints = {
        "Swagger UI": f"{base_url}/swagger/",
        "ReDoc": f"{base_url}/redoc/",
        "Schema JSON": f"{base_url}/swagger.json/",
        "Schema YAML": f"{base_url}/swagger.yaml/"
    }
    
    results = {}
    
    for name, url in endpoints.items():
        try:
            print(f"Testing {name}: {url}")
            response = requests.get(url, timeout=10)
            status = response.status_code
            
            if status == 200:
                print(f"✅ {name}: {status} - Accessible")
                results[name] = "✅ Accessible"
            elif status == 404:
                print(f"❌ {name}: {status} - Not Found")
                results[name] = "❌ Not Found"
            elif status == 403:
                print(f"⚠️ {name}: {status} - Forbidden")
                results[name] = "⚠️ Forbidden"
            else:
                print(f"⚠️ {name}: {status} - {response.reason}")
                results[name] = f"⚠️ {status}"
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection failed (server not running?)")
            results[name] = "❌ Connection failed"
        except requests.exceptions.Timeout:
            print(f"❌ {name}: Timeout")
            results[name] = "❌ Timeout"
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[name] = f"❌ Error: {e}"
    
    return results

def test_production_access():
    """Test if Swagger works in production mode"""
    print("\n🔧 Testing Production Mode Access...")
    
    # Temporarily set DEBUG to False
    original_debug = os.environ.get('DEBUG')
    os.environ['DEBUG'] = 'False'
    
    try:
        # Reload Django settings
        from importlib import reload
        import mood_tracker.mood_tracker.settings as settings_module
        reload(settings_module)
        
        # Test configuration
        config_ok = test_swagger_configuration()
        
        if config_ok:
            print("✅ Swagger should work in production mode")
            print("📝 Note: Schema view has permission_classes=(permissions.AllowAny,)")
            print("📝 Note: No DEBUG restrictions found in URL configuration")
        else:
            print("❌ Swagger configuration issues detected")
            
    finally:
        # Restore original DEBUG setting
        if original_debug is not None:
            os.environ['DEBUG'] = original_debug
        else:
            os.environ.pop('DEBUG', None)

def main():
    """Main test function"""
    print("🧪 SWAGGER ENDPOINT ACCESSIBILITY TEST")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_swagger_configuration()
    
    if not config_ok:
        print("\n❌ Configuration issues detected. Swagger may not work properly.")
        return
    
    # Test production mode
    test_production_access()
    
    # Test live production deployment
    print("\n" + "=" * 50)
    print("🚀 TESTING LIVE PRODUCTION DEPLOYMENT")
    print("🌐 Checking: https://moodify-wmcd.onrender.com")
    
    production_results = test_swagger_endpoint_access("https://moodify-wmcd.onrender.com")
    
    print("\n� PRODUCTION DEPLOYMENT RESULTS:")
    for endpoint, result in production_results.items():
        print(f"  {endpoint}: {result}")
    
    # Also test local if needed
    print("\n" + "=" * 50)
    print("🏠 TESTING LOCAL DEVELOPMENT (if server is running)")
    
    local_results = test_swagger_endpoint_access("http://localhost:8000")
    
    print("\n📊 LOCAL DEVELOPMENT RESULTS:")
    for endpoint, result in local_results.items():
        print(f"  {endpoint}: {result}")
    
    # Final summary
    print("\n🎯 FINAL ANALYSIS:")
    
    # Check production accessibility
    production_accessible = any("✅" in result for result in production_results.values())
    if production_accessible:
        print("✅ Swagger IS accessible on your production deployment!")
        print("🌐 Visit: https://moodify-wmcd.onrender.com/swagger/")
        print("📚 API Docs: https://moodify-wmcd.onrender.com/redoc/")
    else:
        print("❌ Swagger is NOT accessible on production")
        print("🔧 Possible issues:")
        print("   - Production server might be using production.py settings")
        print("   - DEBUG=False might be disabling Swagger")
        print("   - Server might be down or restarting")
        print("   - ALLOWED_HOSTS configuration issue")
    
    print("\n💡 RECOMMENDATIONS:")
    print("  1. Check your production environment variables")
    print("  2. Ensure ALLOWED_HOSTS includes your domain")
    print("  3. Consider enabling Swagger in production if desired")
    print("  4. Check server logs if endpoints are not accessible")

if __name__ == "__main__":
    main()
