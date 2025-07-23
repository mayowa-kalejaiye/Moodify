#!/usr/bin/env python
import os
import sys

# Simple test to check if Django is working
print("Testing Django setup...")

# Set up the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

# Try to import Django
try:
    import django
    print(f"✅ Django imported successfully, version: {django.get_version()}")
except ImportError as e:
    print(f"❌ Failed to import Django: {e}")
    sys.exit(1)

# Try to setup Django
try:
    django.setup()
    print("✅ Django setup completed successfully")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Try to import the models
try:
    from mood_tracker.tracker.models import Profile, Challenge, CoinTransaction
    print("✅ Successfully imported all models")
except ImportError as e:
    print(f"❌ Failed to import models: {e}")
    sys.exit(1)

# Test the Challenge model specifically
try:
    # Test basic query
    challenge_count = Challenge.objects.count()
    print(f"✅ Challenge.objects.count() = {challenge_count}")
    
    # Test settled field query
    settled_count = Challenge.objects.filter(settled=True).count()
    print(f"✅ Challenge.objects.filter(settled=True).count() = {settled_count}")
    
    unsettled_count = Challenge.objects.filter(settled=False).count()
    print(f"✅ Challenge.objects.filter(settled=False).count() = {unsettled_count}")
    
    print("\n🎉 ALL TESTS PASSED! Django and the Challenge model are working correctly.")
    print("The 'settled' column is properly accessible from Django ORM.")
    
except Exception as e:
    print(f"❌ Error testing Challenge model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
