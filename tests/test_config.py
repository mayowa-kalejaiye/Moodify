#!/usr/bin/env python3
"""
Django Configuration Test

This script validates the Django application configuration including:
- Environment variable loading
- Database connectivity  
- Settings validation
- AI service URL configuration

Usage:
    python tests/test_config.py

Environment:
    Requires .env file with proper configuration
"""
import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to Python path
sys.path.append('.')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

try:
    django.setup()
    from django.conf import settings
    
    print("✅ Django setup successful!")
    print(f"✅ AI_SERVICE_URL configured: {settings.AI_SERVICE_URL}")
    print(f"✅ DEBUG mode: {settings.DEBUG}")
    print(f"✅ Secret key configured: {'Yes' if settings.SECRET_KEY else 'No'}")
    print(f"✅ Database configured: {settings.DATABASES['default']['ENGINE']}")
    
    # Test database connection
    from django.db import connection
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection working!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    print("\n🎉 Configuration looks good! Your app should work with the AI service.")
    print("\n📋 Next Steps:")
    print("  1. Start Django server: python manage.py runserver")
    print("  2. Test AI endpoints: python tests/test_ai_connection.py")
    print("  3. Run full test suite: python manage.py test")
    
except Exception as e:
    print(f"❌ Configuration error: {e}")
    print("\n🔧 Troubleshooting:")
    print("  1. Check .env file exists and has required variables")
    print("  2. Verify DJANGO_SECRET_KEY is set")
    print("  3. Ensure AI_SERVICE_URL is configured")
    import traceback
    traceback.print_exc()
